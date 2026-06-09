"""
views.py - Dashboard Page Layouts.

Orchestrates metrics, charts, and funnel logic into structured Streamlit views.
Each view receives the cleaned DataFrame and an active FilterState, applies
filters before querying DuckDB, then composes the UI from chart + metric primitives.

Views:
    show_overview()          → KPIs + revenue bar + deal stage bar + trend line
    show_regional_breakdown()→ Heatmap + regional revenue bar + rep scatter
    show_funnel_analysis()   → Funnel chart + conversion KPIs + drop-off table
    show_rep_performance()   → Rep leaderboard + top/bottom rankings + scorecard
"""

import streamlit as st
import polars as pl
from typing import Optional

from db import db_engine
from metrics import SalesMetrics
from charts import ChartFactory
from funnel import SalesFunnel
from filters import FilterState
from theme import section_header, status_badge


# ══════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════

def _apply_filters(df: pl.DataFrame, fs: FilterState) -> pl.DataFrame:
    """
    Applies the active FilterState to a Polars DataFrame in-memory.
    Used for chart data before re-querying DuckDB with filtered slice.

    Args:
        df: Full cleaned DataFrame
        fs: Active FilterState from SidebarFilters.render()

    Returns:
        Filtered Polars DataFrame
    """
    filtered = df

    # Date range
    filtered = filtered.filter(
        (pl.col("date") >= fs.start_date) &
        (pl.col("date") <= fs.end_date)
    )

    # Regions
    if fs.selected_regions:
        filtered = filtered.filter(pl.col("region").is_in(fs.selected_regions))

    # Reps
    if fs.selected_reps:
        filtered = filtered.filter(pl.col("rep").is_in(fs.selected_reps))

    # Minimum revenue
    if fs.min_revenue > 0:
        filtered = filtered.filter(pl.col("revenue") >= fs.min_revenue)

    return filtered


def _metric_card(col, label: str, value: str, delta: Optional[str] = None) -> None:
    """Renders a single st.metric KPI card."""
    if delta:
        col.metric(label, value, delta)
    else:
        col.metric(label, value)


def _no_data_warning(context: str = "") -> None:
    """Renders a styled empty-state warning."""
    st.markdown(
        f"""
        <div style="
            background:rgba(5,150,105,0.06);
            border:1px solid rgba(5,150,105,0.2);
            border-radius:14px;
            padding:2rem;
            text-align:center;
            font-family:Inter,sans-serif;
        ">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📭</div>
            <div style="color:#94A3B8;font-size:0.9rem;">
                No data available{f' for {context}' if context else ''}.
                <br>Try adjusting your filters.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════
# VIEW 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════

class DashboardViews:

    @staticmethod
    def show_overview(df: pl.DataFrame, filter_state: FilterState) -> None:
        """
        Renders the Sales Overview tab.

        Sections:
            1. KPI metric strip  (Total Revenue, Deals, Avg Deal Size, MoM Growth)
            2. Revenue by Region (bar chart)
            3. Deals by Stage   (bar chart — uses bar_count())
            4. Revenue Trend    (line chart)
        """
        section_header("Sales Overview", "High-level performance metrics across all dimensions")

        # ── Apply filters ──
        filtered = _apply_filters(df, filter_state)

        if filtered.is_empty():
            _no_data_warning("the selected filters")
            return

        # ── Seed DuckDB with filtered slice ──
        db_engine.seed_data(filtered)

        # ── 1. KPI Metrics ──
        total_rev   = filtered["revenue"].sum()
        total_deals = filtered.shape[0]
        avg_deal    = total_rev / total_deals if total_deals > 0 else 0
        regions     = filtered["region"].n_unique()

        # Month-over-month growth
        monthly_df = (
            filtered
            .with_columns(pl.col("date").dt.truncate("1mo").alias("month"))
            .group_by("month")
            .agg(pl.sum("revenue").alias("revenue"))
            .sort("month")
        )
        mom = SalesMetrics.calculate_mom_growth(monthly_df)
        growth_pct  = mom.get("growth_pct", 0.0)
        growth_sign = "+" if growth_pct >= 0 else ""
        growth_str  = f"{growth_sign}{growth_pct:.1f}%"

        c1, c2, c3, c4 = st.columns(4)
        _metric_card(c1, "Total Revenue",    f"${total_rev:,.0f}",    growth_str)
        _metric_card(c2, "Total Deals",      f"{total_deals:,}")
        _metric_card(c3, "Avg Deal Size",    f"${avg_deal:,.0f}")
        _metric_card(c4, "Active Regions",   f"{regions}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. Revenue by Region + Deals by Stage ──
        rev_by_region = db_engine.get_revenue_by_dimension("region")
        stage_counts  = db_engine.get_stage_counts()

        c_left, c_right = st.columns(2, gap="medium")

        with c_left:
            section_header("Revenue by Region", "")
            if not rev_by_region.is_empty():
                fig = ChartFactory.bar_revenue(rev_by_region, "region", "Revenue by Region")
                st.plotly_chart(fig, use_container_width=True)
            else:
                _no_data_warning("regions")

        with c_right:
            section_header("Deals by Stage", "")
            if not stage_counts.is_empty():
                fig = ChartFactory.bar_count(stage_counts, "stage", "deal_count", "Deals by Stage")
                st.plotly_chart(fig, use_container_width=True)
            else:
                _no_data_warning("stages")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. Revenue Trend ──
        section_header("Revenue Trend", "Monthly aggregation over selected date range")

        if not monthly_df.is_empty():
            fig_trend = ChartFactory.line_trend(monthly_df, "Monthly Revenue Trend")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            _no_data_warning("the trend chart")


    # ══════════════════════════════════════════════════════════════
    # VIEW 2 — REGIONAL BREAKDOWN
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def show_regional_breakdown(df: pl.DataFrame, filter_state: FilterState) -> None:
        """
        Renders the Regional Breakdown tab.

        Sections:
            1. KPIs  (Best Region, Best Rep, Total Deals in Range)
            2. Heatmap — Revenue density across Reps × Regions
            3. Revenue by Region (bar — re-confirms top regions)
            4. Rep scatter across deal sizes
        """
        section_header("Regional Performance", "Revenue density and geographic breakdown")

        # ── Apply filters ──
        filtered = _apply_filters(df, filter_state)

        if filtered.is_empty():
            _no_data_warning("the selected region/date filters")
            return

        db_engine.seed_data(filtered)

        # ── 1. Regional KPIs ──
        rev_by_region = db_engine.get_revenue_by_dimension("region")

        if not rev_by_region.is_empty():
            best_region     = rev_by_region["region"][0]
            best_region_rev = rev_by_region["total_revenue"][0]
        else:
            best_region, best_region_rev = "—", 0

        rev_by_rep = db_engine.get_revenue_by_dimension("rep")
        if not rev_by_rep.is_empty():
            best_rep     = rev_by_rep["rep"][0]
            best_rep_rev = rev_by_rep["total_revenue"][0]
        else:
            best_rep, best_rep_rev = "—", 0

        c1, c2, c3 = st.columns(3)
        _metric_card(c1, "Top Region",    best_region,          f"${best_region_rev:,.0f}")
        _metric_card(c2, "Top Rep",       best_rep,             f"${best_rep_rev:,.0f}")
        _metric_card(c3, "Total Deals",   f"{filtered.shape[0]:,}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. Heatmap: Reps × Regions ──
        section_header("Revenue Density Heatmap", "Rep performance across all regions")

        heatmap_data = (
            filtered
            .group_by(["rep", "region"])
            .agg(pl.sum("revenue").alias("revenue"))
        )

        if not heatmap_data.is_empty():
            fig_heat = ChartFactory.heatmap_rep_region(heatmap_data)
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            _no_data_warning("the heatmap")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. Revenue by Region bar ──
        section_header("Revenue by Region", "")

        c_left, c_right = st.columns(2, gap="medium")

        with c_left:
            if not rev_by_region.is_empty():
                fig = ChartFactory.bar_revenue(rev_by_region, "region", "Revenue by Region")
                st.plotly_chart(fig, use_container_width=True)

        with c_right:
            section_header("Revenue by Rep", "")
            if not rev_by_rep.is_empty():
                fig = ChartFactory.bar_revenue(rev_by_rep, "rep", "Revenue by Rep")
                st.plotly_chart(fig, use_container_width=True)


    # ══════════════════════════════════════════════════════════════
    # VIEW 3 — FUNNEL ANALYSIS
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def show_funnel_analysis(df: pl.DataFrame, filter_state: FilterState) -> None:
        """
        Renders the Pipeline Funnel tab.

        Sections:
            1. Funnel KPIs  (Total Deals, Closed, Overall Conversion %)
            2. Funnel chart (Plotly Funnel with Emerald → Gold gradient)
            3. Drop-off table (stage-by-stage conversion breakdown)
        """
        section_header("Pipeline Conversion", "Stage-by-stage deal flow and drop-off analysis")

        # ── Apply filters ──
        filtered = _apply_filters(df, filter_state)

        if filtered.is_empty():
            _no_data_warning("the funnel")
            return

        # ── Process funnel ──
        funnel_df = SalesFunnel.process_funnel_data(filtered)

        if funnel_df.is_empty():
            _no_data_warning("the funnel")
            return

        # ── 1. Funnel KPIs ──
        metrics = SalesFunnel.get_stage_metrics(funnel_df)

        total_deals       = metrics.get("total_deals", 0)
        closed_deals      = metrics.get("closed_deals", 0)
        overall_conv      = metrics.get("overall_conversion_pct", 0.0)
        largest_drop      = metrics.get("largest_drop", 0.0)

        c1, c2, c3, c4 = st.columns(4)
        _metric_card(c1, "Total Deals",         f"{total_deals:,}")
        _metric_card(c2, "Closed Won",          f"{closed_deals:,}")
        _metric_card(c3, "Overall Conversion",  f"{overall_conv:.1f}%")
        _metric_card(c4, "Largest Drop-off",    f"{largest_drop:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. Funnel chart ──
        section_header("Sales Pipeline Funnel", "")

        fig_funnel = SalesFunnel.create_funnel_chart(
            funnel_df,
            title="Pipeline Conversion — Prospecting → Closed Won"
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. Drop-off breakdown table ──
        section_header("Stage-by-Stage Breakdown", "Conversion rates at each pipeline step")

        display_df = funnel_df.select([
            pl.col("stage"),
            pl.col("deal_count"),
            pl.col("cumulative_pct").alias("% of Pipeline")
                if "cumulative_pct" in funnel_df.columns
                else pl.lit(None).alias("% of Pipeline")
        ])

        st.dataframe(
            display_df.to_pandas(),
            use_container_width=True,
            hide_index=True
        )


    # ══════════════════════════════════════════════════════════════
    # VIEW 4 — REP PERFORMANCE
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def show_rep_performance(df: pl.DataFrame, filter_state: FilterState) -> None:
        """
        Renders the Rep Performance tab.

        Sections:
            1. Rep KPIs  (Best Rep, Worst Rep, Total Reps)
            2. Top 5 Performers bar chart
            3. Bottom 5 Performers bar chart
            4. Full leaderboard table with deal counts + avg deal size
        """
        section_header("Rep Performance", "Individual sales representative scorecard and rankings")

        # ── Apply filters ──
        filtered = _apply_filters(df, filter_state)

        if filtered.is_empty():
            _no_data_warning("rep performance")
            return

        db_engine.seed_data(filtered)
        rep_df = db_engine.get_revenue_by_dimension("rep")

        if rep_df.is_empty():
            _no_data_warning("rep performance")
            return

        # ── Rankings from metrics.py ──
        rankings = SalesMetrics.get_rankings(rep_df, "rep", top_n=5)
        top_reps    = rankings["top"]
        bottom_reps = rankings["bottom"]

        # ── 1. Rep KPIs ──
        total_reps = rep_df.shape[0]
        best_rep   = rep_df["rep"][0]   if "rep"   in rep_df.columns else "—"
        best_rev   = rep_df["total_revenue"][0] if not rep_df.is_empty() else 0
        worst_rep  = rep_df["rep"][-1]  if "rep"   in rep_df.columns else "—"
        worst_rev  = rep_df["total_revenue"][-1] if not rep_df.is_empty() else 0

        c1, c2, c3 = st.columns(3)
        _metric_card(c1, "🥇 Top Performer",   best_rep,  f"${best_rev:,.0f}")
        _metric_card(c2, "⚠️ Needs Attention", worst_rep, f"${worst_rev:,.0f}")
        _metric_card(c3, "Total Reps",          f"{total_reps}")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 2. Top 5 vs Bottom 5 ──
        c_left, c_right = st.columns(2, gap="medium")

        with c_left:
            section_header("Top 5 Performers", "")
            if not top_reps.is_empty():
                fig_top = ChartFactory.bar_revenue(top_reps, "rep", "Top 5 Reps by Revenue")
                st.plotly_chart(fig_top, use_container_width=True)

        with c_right:
            section_header("Bottom 5 Performers", "")
            if not bottom_reps.is_empty():
                fig_bot = ChartFactory.bar_revenue(bottom_reps, "rep", "Bottom 5 Reps by Revenue")
                st.plotly_chart(fig_bot, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 3. Full leaderboard table ──
        section_header("Full Leaderboard", "All reps ranked by total revenue")

        leaderboard = (
            filtered
            .group_by("rep")
            .agg([
                pl.sum("revenue").alias("Total Revenue ($)"),
                pl.count("revenue").alias("Deals"),
                (pl.sum("revenue") / pl.count("revenue")).round(0).alias("Avg Deal Size ($)")
            ])
            .sort("Total Revenue ($)", descending=True)
            .with_row_index(name="Rank", offset=1)
        )

        st.dataframe(
            leaderboard.to_pandas(),
            use_container_width=True,
            hide_index=True
        )
