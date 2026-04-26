"""
charts.py - The Plotly Visual Factory.
Generates pre-styled, branded figures for the Sales Dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import polars as pl
from typing import Optional

class ChartFactory:
    # Standard branded color sequence derived from theme.py logic
    COLORS = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

    @staticmethod
    def bar_revenue(df: pl.DataFrame, x_col: str, title: str) -> go.Figure:
        """Generates a vertical bar chart for revenue by dimension."""
        if df.is_empty():
            return go.Figure()

        fig = px.bar(
            df.to_pandas(), 
            x=x_col, 
            y="total_revenue",
            title=title,
            template="plotly_dark",
            color_discrete_sequence=ChartFactory.COLORS
        )
        
        fig.update_layout(xaxis_title=x_col.title(), yaxis_title="Revenue ($)")
        return fig

    @staticmethod
    def line_trend(df: pl.DataFrame, title: str) -> go.Figure:
        """Generates a time-series line chart for revenue trends."""
        if df.is_empty():
            return go.Figure()

        fig = px.line(
            df.to_pandas(),
            x="date",
            y="revenue",
            title=title,
            template="plotly_dark",
            line_shape="spline", # Smooth curves for professional look
            render_mode="svg"
        )
        
        fig.update_traces(line=dict(width=3, color="#00CC96"))
        fig.update_layout(hovermode="x unified")
        return fig

    @staticmethod
    def heatmap_rep_region(df: pl.DataFrame) -> go.Figure:
        """Generates a heatmap showing Rep performance across different Regions."""
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
            color_continuous_scale="Viridis",
            title="Revenue Density: Reps vs Regions",
            template="plotly_dark"
        )
        
        return fig

# Usage Example:
# fig = ChartFactory.bar_revenue(region_data, "region", "Revenue by Territory")
