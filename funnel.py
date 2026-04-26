"""
funnel.py - Specialized Sales Funnel Analytics.
Calculates stage conversion rates and generates branded Plotly funnel charts.
"""

import plotly.graph_objects as go
import polars as pl
from typing import Dict, Any, List

class SalesFunnel:
    # Strict logical order of sales stages
    STAGE_ORDER = ["Lead", "Discovery", "Qualified", "Proposal", "Negotiation", "Closed Won"]

    @staticmethod
    def process_funnel_data(df: pl.DataFrame) -> pl.DataFrame:
        """
        Groups data by stage and ensures logical ordering and conversion math.
        """
        if df.is_empty():
            return pl.DataFrame()

        # Group by stage and count deals
        summary = (
            df.group_by("stage")
            .agg(pl.count("stage").alias("deal_count"))
            .to_pandas()
        )

        # Reindex to match the STAGE_ORDER and handle missing stages
        summary['stage'] = summary['stage'].astype('category')
        summary['stage'] = summary['stage'].cat.set_categories(SalesFunnel.STAGE_ORDER, ordered=True)
        summary = summary.sort_values("stage").dropna(subset=["stage"])

        # Calculate Drop-off (Percentage of the previous stage)
        summary['conversion_rate'] = summary['deal_count'].pct_change().fillna(0) * 100
        
        return pl.from_pandas(summary)

    @staticmethod
    def create_funnel_chart(funnel_df: pl.DataFrame) -> go.Figure:
        """
        Creates a branded Plotly funnel chart.
        """
        if funnel_df.is_empty():
            return go.Figure()

        fig = go.Figure(go.Funnel(
            y=funnel_df["stage"].to_list(),
            x=funnel_df["deal_count"].to_list(),
            textinfo="value+percent initial",
            marker={"color": ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3"]},
            connector={"line": {"color": "white", "width": 2}}
        ))

        fig.update_layout(
            title_text="Sales Pipeline Conversion",
            template="plotly_dark", # Aligns with your theme.py
            margin=dict(l=20, r=20, t=50, b=20)
        )

        return fig

# Usage:
# funnel_logic = SalesFunnel()
# clean_funnel_df = funnel_logic.process_funnel_data(db_results)
# fig = funnel_logic.create_funnel_chart(clean_funnel_df)
