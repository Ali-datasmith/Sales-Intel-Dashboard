"""
transform.py - Data Cleaning & Normalization Layer.
Uses Polars for high-speed vectorized transformations and type coercion.
"""

import polars as pl
import re
from typing import Optional

class DataTransformer:
    @staticmethod
    def clean_data(df: pl.DataFrame) -> pl.DataFrame:
        """
        Orchestrates the full transformation pipeline.
        
        Args:
            df: Raw Polars DataFrame from ingest.py
            
        Returns:
            pl.DataFrame: Cleaned, typed, and normalized DataFrame.
        """
        if df.is_empty():
            return df

        return (
            df.pipe(DataTransformer._normalize_column_names)
              .pipe(DataTransformer._handle_duplicates)
              .pipe(DataTransformer._coerce_types)
              .pipe(DataTransformer._handle_nulls)
        )

    @staticmethod
    def _normalize_column_names(df: pl.DataFrame) -> pl.DataFrame:
        """Standardizes column names: lowercase and removes special chars/spaces."""
        return df.rename({
            col: re.sub(r'[^a-z0-9_]', '', col.lower().strip().replace(" ", "_")) 
            for col in df.columns
        })

    @staticmethod
    def _handle_duplicates(df: pl.DataFrame) -> pl.DataFrame:
        """Removes exact duplicate rows."""
        return df.unique()

    @staticmethod
    def _coerce_types(df: pl.DataFrame) -> pl.DataFrame:
        """Fixes dates and cleans currency/numeric strings."""
        
        # 1. Clean Revenue: Remove $, commas, and cast to Float64
        if "revenue" in df.columns:
            if df["revenue"].dtype == pl.Utf8:
                df = df.with_columns(
                    pl.col("revenue")
                    .str.replace_all(r"[$, ]", "")
                    .cast(pl.Float64, strict=False)
                    .fill_null(0.0)
                )

        # 2. Robust Date Parsing
        if "date" in df.columns:
            # Attempt to parse common formats; strict=False turns failures to Null
            df = df.with_columns(
                pl.col("date").str.to_date(strict=False)
            )
            # Drop rows where date couldn't be parsed to prevent DB errors
            df = df.filter(pl.col("date").is_not_null())

        return df

    @staticmethod
    def _handle_nulls(df: pl.DataFrame) -> pl.DataFrame:
        """Fills missing categorical data with placeholders."""
        categorical_cols = ["rep", "region", "product", "stage"]
        
        for col in categorical_cols:
            if col in df.columns:
                df = df.with_columns(
                    pl.col(col).fill_null("Unknown")
                )
        return df

# Usage: 
# clean_df = DataTransformer.clean_data(raw_df)
