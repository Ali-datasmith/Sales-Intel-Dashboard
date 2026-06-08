"""
charts.py - The Plotly Visual Factory.
Generates pre-styled, branded figures for the Sales Dashboard.

Uses the custom 'sales_intel_dark' theme from theme.py with Emerald + Gold palette.
"""

import plotly.graph_objects as go
import plotly.express as px
import polars as pl
from typing import Optional

# ── Theme Colors (Emerald + Gold) ──
PRIMARY_EMERALD = "#059669"      # Deep Emerald - primary brand color
ACCENT_GOLD = "#FBBF24"           # Gold - success/premium accent
SECONDARY_TEAL = "#0D9488"        # Teal - secondary data
DANGER_RED = "#DC2626"            # Red - alerts/negatives
SUCCESS_GREEN = "#10B981"         # Green - positive metrics
LIGHT_SLATE = "#F1F5F9"           # Light text on dark

class ChartFactory:
    """
    Factory for generating branded Plotly charts.
    All charts use the 'sales_intel_dark' custom template from theme.py
    """
    
    # Primary color sequence: Emerald → Gold → Teal → Secondary shades
    COLORS = [
        PRIMARY_EMERALD,    # #059669 - Primary Emerald
        ACCENT_GOLD,        # #FBBF24 - Gold accent
        SECONDARY_TEAL,     # #0D9488 - Teal
        "#047857",          # Darker Emerald
        "#D97706"           # Amber (complements Gold)
    ]

    @staticmethod
    def bar_revenue(df: pl.DataFrame, x_col: str, title: str) -> go.Figure:
        """
        Generates a vertical bar chart for revenue aggregations.
        
        Args:
            df: Polars DataFrame with 'total_revenue' and dimension column
            x_col: Column name for X-axis grouping
            title: Chart title
            
        Returns:
            go.Figure with professional styling
        """
        if df.is_empty():
            return go.Figure()

        fig = px.bar(
            df.to_pandas(),
            x=x_col,
            y="total_revenue",
            title=title,
            template="plotly_dark",  # Will be overridden by sales_intel_dark in app
            color_discrete_sequence=ChartFactory.COLORS
        )

        fig.update_layout(
            xaxis_title=x_col.title(),
            yaxis_title="Revenue ($)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=LIGHT_SLATE),
            hovermode="x unified",
            showlegend=False
        )
        
        # Highlight bars with Emerald
        fig.update_traces(
            marker=dict(
                color=PRIMARY_EMERALD,
                line=dict(color=ACCENT_GOLD, width=1),
                opacity=0.85
            ),
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
        )
        
        return fig

    @staticmethod
    def bar_count(df: pl.DataFrame, x_col: str, count_col: str, title: str) -> go.Figure:
        """
        Generates a vertical bar chart for count/deal metrics.
        Alternative to bar_revenue for non-monetary aggregations.
        
        Args:
            df: Polars DataFrame with count/deal_count column
            x_col: Column name for X-axis grouping
            count_col: Column name for Y-axis (e.g., 'deal_count')
            title: Chart title
            
        Returns:
            go.Figure with professional styling
        """
        if df.is_empty():
            return go.Figure()

        fig = px.bar(
            df.to_pandas(),
            x=x_col,
            y=count_col,
            title=title,
            template="plotly_dark",
            color_discrete_sequence=[SECONDARY_TEAL]
        )

        fig.update_layout(
            xaxis_title=x_col.title(),
            yaxis_title=count_col.replace("_", " ").title(),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=LIGHT_SLATE),
            hovermode="x unified",
            showlegend=False
        )
        
        fig.update_traces(
            marker=dict(
                color=SECONDARY_TEAL,
                line=dict(color=ACCENT_GOLD, width=1),
                opacity=0.85
            ),
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>"
        )
        
        return fig

    @staticmethod
    def line_trend(df: pl.DataFrame, title: str) -> go.Figure:
        """
        Generates a time-series line chart for revenue/metric trends.
        
        Args:
            df: Polars DataFrame with 'date' and 'revenue' columns
            title: Chart title
            
        Returns:
            go.Figure with smooth spline interpolation
        """
        if df.is_empty():
            return go.Figure()

        fig = px.line(
            df.to_pandas(),
            x="date",
            y="revenue",
            title=title,
            template="plotly_dark",
            line_shape="spline",  # Smooth curves
            render_mode="svg"
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=LIGHT_SLATE),
            hovermode="x unified",
            xaxis_title="Date",
            yaxis_title="Revenue ($)"
        )
        
        fig.update_traces(
            line=dict(width=3, color=PRIMARY_EMERALD),
            fill="tozeroy",
            fillcolor="rgba(5, 150, 105, 0.1)",  # Emerald with transparency
            hovertemplate="<b>%{x|%B %d, %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>"
        )
        
        return fig

    @staticmethod
    def heatmap_rep_region(df: pl.DataFrame) -> go.Figure:
        """
        Generates a heatmap showing Rep performance across Regions.
        
        Args:
            df: Polars DataFrame with 'rep', 'region', 'revenue' columns
            
        Returns:
            go.Figure with Emerald-to-Gold color scale
        """
        if df.is_empty():
            return go.Figure()

        # Pivot data for heatmap format
        pivot_df = df.pivot(
            values="revenue",
            index="rep",
            on="region",
            aggregate_function="sum"
        ).fill_null(0).to_pandas().set_index("rep")

        fig = px.imshow(
            pivot_df,
            labels=dict(x="Region", y="Sales Rep", color="Revenue"),
            color_continuous_scale=[
                [0.0, "#E0F2FE"],      # Light blue (low values)
                [0.5, PRIMARY_EMERALD], # Emerald (mid values)
                [1.0, ACCENT_GOLD]      # Gold (high values)
            ],
            title="Revenue Density: Reps vs Regions",
            template="plotly_dark",
            text_auto=".0f"
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=LIGHT_SLATE),
            color_continuous_colorbar=dict(
                title="Revenue ($)",
                tickprefix="$"
            )
        )
        
        fig.update_traces(
            hovertemplate="<b>%{y} × %{x}</b><br>Revenue: $%{z:,.0f}<extra></extra>"
        )
        
        return fig

    @staticmethod
    def scatter_pipeline(df: pl.DataFrame, title: str = "Deal Pipeline") -> go.Figure:
        """
        Generates a scatter plot for deal stage vs revenue analysis.
        Useful for identifying pipeline velocity and deal sizes.
        
        Args:
            df: Polars DataFrame with 'stage', 'revenue', and count columns
            title: Chart title
            
        Returns:
            go.Figure with bubble sizing
        """
        if df.is_empty():
            return go.Figure()

        fig = px.scatter(
            df.to_pandas(),
            x="stage",
            y="revenue",
            size="deal_count" if "deal_count" in df.columns else "revenue",
            color="stage",
            title=title,
            template="plotly_dark",
            color_discrete_sequence=ChartFactory.COLORS
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=LIGHT_SLATE),
            hovermode="closest",
            showlegend=False
        )
        
        return fig


# ── Theme Color Reference ──
# PRIMARY_EMERALD (#059669): Main brand color for primary metrics
# ACCENT_GOLD (#FBBF24):      Highlights, success indicators, premium elements
# SECONDARY_TEAL (#0D9488):  Secondary data series, supporting visuals
# Use sparingly with high contrast on dark backgrounds for accessibility
