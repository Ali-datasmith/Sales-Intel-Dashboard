"""
db.py - The analytical engine for SalesIntelDashboard.
Uses DuckDB to run high-speed SQL aggregations on in-memory Polars DataFrames.
"""

import duckdb
import polars as pl
from typing import Optional, List

class SalesDB:
    def __init__(self):
        """Initializes an in-process DuckDB connection."""
        self.con = duckdb.connect(database=":memory:")

    def seed_data(self, df: pl.DataFrame) -> None:
        """
        Registers a Polars DataFrame as a virtual table named 'sales_data'.
        
        Args:
            df: The cleaned Polars DataFrame from transform.py
        """
        if df.is_empty():
            raise ValueError("Cannot seed database with an empty DataFrame.")
            
        # DuckDB can query Polars objects directly if they are in the local scope
        self.con.register("sales_data", df)

    def get_revenue_by_dimension(self, dimension: str) -> pl.DataFrame:
        """
        Aggregates revenue based on a specific dimension (e.g., 'region', 'rep').
        
        Input: dimension="region"
        Output: pl.DataFrame([region, total_revenue])
        """
        # Note: Dimension is validated against a whitelist to prevent SQL injection
        allowed = {"region", "rep", "product", "stage"}
        if dimension not in allowed:
            raise ValueError(f"Invalid dimension: {dimension}")

        query = f"""
            SELECT {dimension}, SUM(revenue) as total_revenue
            FROM sales_data
            GROUP BY {dimension}
            ORDER BY total_revenue DESC
        """
        return self.con.execute(query).pl()

    def get_date_range_slice(self, start_date: str, end_date: str) -> pl.DataFrame:
        """
        Filters data by a date range and returns the full slice.
        
        Input: start_date="2024-01-01", end_date="2024-03-31"
        Output: pl.DataFrame of transactions within range
        """
        query = """
            SELECT * FROM sales_data 
            WHERE date >= ? AND date <= ?
        """
        return self.con.execute(query, [start_date, end_date]).pl()

    def get_stage_counts(self) -> pl.DataFrame:
        """
        Returns count of deals per stage for funnel visualization.
        """
        query = """
            SELECT stage, COUNT(*) as deal_count
            FROM sales_data
            GROUP BY stage
            ORDER BY deal_count DESC
        """
        return self.con.execute(query).pl()

# Singleton instance for the app
db_engine = SalesDB()
