"""
views.py - Dashboard Page Layouts.
Orchestrates metrics, charts, and funnel logic into structured Streamlit views.
"""

import streamlit as st
import polars as pl
from db import db_engine
from metrics import SalesMetrics
from charts import ChartFactory
from funnel import SalesFunnel

class DashboardViews:
    @staticmethod
    def show_overview():
        """Renders the main dashboard with high-level KPIs and trends."""
        st.subheader("🚀 Sales Overview")
        
        # 1. Fetch Data
        df = db_engine.get_revenue_by_dimension("region")
        total_rev = df["total_revenue"].sum()
        
        # 2. KPI Metrics Bar
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"${total_rev:,.0f}")
        col2.metric("Active Regions", len(df))
        col3.metric("Goal Attainment", "84%") # Example static target

        # 3. Charts Row
        c1, c2 = st.columns(2)
        with c1:
            fig_rev = ChartFactory.bar_revenue(df, "region", "Revenue by Region")
            st.plotly_chart(fig_rev, use_container_width=True)
        with c2:
            # Using stage counts for overview
            stage_df = db_engine.get_stage_counts()
            fig_stage = ChartFactory.bar_revenue(stage_df.rename({"deal_count": "total_revenue"}), "stage", "Deals by Stage")
            st.plotly_chart(fig_stage, use_container_width=True)

    @staticmethod
    def show_regional_breakdown():
        """Renders deep-dive into regional density and heatmaps."""
        st.subheader("📍 Regional Performance")
        
        # Using a raw slice for the heatmap
        raw_data = db_engine.get_date_range_slice("2000-01-01", "2099-12-31")
        
        fig_heat = ChartFactory.heatmap_rep_region(raw_data)
        st.plotly_chart(fig_heat, use_container_width=True)

    @staticmethod
    def show_funnel_analysis():
        """Renders the sales pipeline funnel and drop-off stats."""
        st.subheader("🌪️ Pipeline Conversion")
        
        # 1. Process Funnel
        raw_data = db_engine.get_date_range_slice("2000-01-01", "2099-12-31")
        funnel_df = SalesFunnel.process_funnel_data(raw_data)
        
        # 2. Render Visual
        fig_funnel = SalesFunnel.create_funnel_chart(funnel_df)
        st.plotly_chart(fig_funnel, use_container_width=True)
        
        # 3. Drop-off Table
        st.dataframe(funnel_df, use_container_width=True)

    @staticmethod
    def show_rep_performance():
        """Renders individual scorecard for sales representatives."""
        st.subheader("👤 Rep Leaderboard")
        
        rep_df = db_engine.get_revenue_by_dimension("rep")
        rankings = SalesMetrics.get_rankings(rep_df)
        
        st.markdown("### Top Performers")
        st.table(rankings["top"].to_pandas())
