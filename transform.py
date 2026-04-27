"""
transform.py - The Data Sanitization Layer.
Uses Polars for high-performance cleaning, schema enforcement, 
and type safety.
"""

import polars as pl
import re
from typing import Optional

class DataTransformer:
    @staticmethod
    def clean_data(df: pl.DataFrame) -> pl.DataFrame:
        """
        Main entry point for the transformation pipeline.
        Executes normalization, type-casting, and null handling.
        """
        if df.is_empty():
            return df

        return (
            df.pipe(DataTransformer._normalize_headers)
              .pipe(DataTransformer._clean_revenue)
              .pipe(DataTransformer._parse_dates)
              .pipe(DataTransformer._handle_categories)
              .unique()
        )

    @staticmethod
    def _normalize_headers(df: pl.DataFrame) -> pl.DataFrame:
        """Standardizes column names to snake_case and removes special characters."""
        new_cols = {
            col: re.sub(r'[^a-z0-9_]', '', col.lower().strip().replace(" ", "_")) 
            for col in df.columns
        }
        return df.rename(new_cols)

    @staticmethod
    def _clean_revenue(df: pl.DataFrame) -> pl.DataFrame:
        """Extracts numeric values from currency strings and ensures Float64."""
        if "revenue" not in df.columns:
            return df
        
        # If data is string (e.g., "$1,200"), strip symbols and cast
        if df["revenue"].dtype == pl.Utf8:
            df = df.with_columns(
                pl.col("revenue")
                .str.replace_all(r"[$, ]", "")
                .cast(pl.Float64, strict=False)
            )
        
        return df.with_columns(pl.col("revenue").fill_null(0.0))

    @staticmethod
    def _parse_dates(df: pl.DataFrame) -> pl.DataFrame:
        """Handles both pre-parsed datetimes and raw string dates."""
        if "date" not in df.columns:
            return df

        # Only parse if column is string; if it's already datetime, Polars handles it
        if df["date"].dtype == pl.Utf8:
            df = df.with_columns(
                pl.col("date").str.to_date(strict=False)
            )
        
        # Ensure we drop invalid dates that couldn't be parsed
        return df.filter(pl.col("date").is_not_null())

    @staticmethod
    def _handle_categories(df: pl.DataFrame) -> pl.DataFrame:
        """Ensures core categorical columns exist and fills missing values."""
        required_cats = ["rep", "region", "product", "stage"]
        
        for col in required_cats:
            if col not in df.columns:
                # Create the column if missing to prevent dashboard crashes
                df = df.with_columns(pl.lit("Unknown").alias(col))
            else:
                df = df.with_columns(pl.col(col).fill_null("Unknown"))
        
        return df
