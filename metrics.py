"""
metrics.py - Business Logic & KPI Calculation Layer.
Processes DuckDB results into actionable insights and alerts.
"""

import polars as pl
from typing import Dict, Any, List

class SalesMetrics:
    @staticmethod
    def calculate_mom_growth(current_df: pl.DataFrame) -> Dict[str, Any]:
        """
        Calculates Month-over-Month growth from a time-series DataFrame.
        Expects columns: ['month', 'revenue']
        """
        if current_df.height < 2:
            return {"growth_pct": 0.0, "is_positive": True}

        # Sort by month to ensure sequence
        df = current_df.sort("month")
        
        # Get last two months
        prev_rev = df["revenue"][-2]
        curr_rev = df["revenue"][-1]

        if prev_rev == 0:
            growth = 100.0 if curr_rev > 0 else 0.0
        else:
            growth = ((curr_rev - prev_rev) / prev_rev) * 100

        return {
            "current_revenue": round(curr_rev, 2),
            "previous_revenue": round(prev_rev, 2),
            "growth_pct": round(growth, 1),
            "is_positive": growth >= 0
        }

    @staticmethod
    def get_variance_alerts(df: pl.DataFrame, threshold: float = -15.0) -> pl.DataFrame:
        """
        Identifies dimensions where revenue has dropped beyond the threshold.
        """
        # This assumes the input DF has a 'variance' or 'growth' column already calculated
        if "growth" not in df.columns:
            return pl.DataFrame()

        return df.filter(pl.col("growth") <= threshold)

    @staticmethod
    def get_rankings(df: pl.DataFrame, dimension: str, top_n: int = 5) -> Dict[str, pl.DataFrame]:
        """
        Returns top and bottom performers for a given dimension.
        """
        if df.is_empty():
            return {"top": pl.DataFrame(), "bottom": pl.DataFrame()}

        sorted_df = df.sort("total_revenue", descending=True)
        
        return {
            "top": sorted_df.head(top_n),
            "bottom": sorted_df.tail(top_n)
        }

    @staticmethod
    def calculate_attainment(actual: float, target: float) -> float:
        """Calculates percentage of goal reached."""
        if target <= 0:
            return 0.0
        return round((actual / target) * 100, 1)

# Example output format for a 'Top Reps' widget:
# Input: pl.DataFrame({"rep": ["Ali", "Sara"], "total_revenue": [5000, 3000]})
# Output: {"top": ..., "bottom": ...}
