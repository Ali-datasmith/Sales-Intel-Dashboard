"""
filters.py - UI Control & State Management Layer.
Manages all Streamlit sidebar widgets and returns a structured FilterState.
"""

import streamlit as st
import polars as pl
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

@dataclass(frozen=True)
class FilterState:
    """Immutable container for all dashboard filter selections."""
    start_date: date
    end_date: date
    selected_regions: List[str]
    selected_reps: List[str]
    min_revenue: float

class SidebarFilters:
    @staticmethod
    def render(df: pl.DataFrame) -> FilterState:
        """
        Renders all sidebar widgets and captures user input.
        
        Args:
            df: The cleaned Polars DataFrame to extract unique values from.
        """
        st.sidebar.header("📊 Dashboard Filters")

        # 1. Date Range Filter
        min_date = df["date"].min()
        max_date = df["date"].max()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Handle Streamlit's date_input return behavior (can be a tuple or single date)
        start_dt, end_dt = (date_range[0], date_range[1]) if len(date_range) == 2 else (min_date, max_date)

        # 2. Multi-select Filters (Dynamic)
        regions = df["region"].unique().sort().to_list()
        selected_regions = st.sidebar.multiselect("Regions", options=regions, default=regions)

        reps = df["rep"].unique().sort().to_list()
        selected_reps = st.sidebar.multiselect("Sales Representatives", options=reps, default=reps)

        # 3. Numeric Threshold
        max_rev = float(df["revenue"].max())
        min_revenue = st.sidebar.slider("Min Revenue Threshold ($)", 0.0, max_rev, 0.0)

        return FilterState(
            start_date=start_dt,
            end_date=end_dt,
            selected_regions=selected_regions,
            selected_reps=selected_reps,
            min_revenue=min_revenue
        )
