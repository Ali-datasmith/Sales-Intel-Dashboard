"""
transform.py - Data Cleaning & Normalization Layer.

Orchestrates a Polars-based transformation pipeline:
    1. Normalize column headers to snake_case
    2. Clean revenue strings → Float64
    3. Parse date strings → pl.Date
    4. Ensure categorical columns exist and fill nulls
    5. Drop exact duplicate rows

Usage:
    clean_df = DataTransformer.clean_data(raw_df)
"""

import re
import polars as pl


class DataTransformer:
    """
    Stateless transformer — all methods are @staticmethod.
    Accepts a raw Polars DataFrame from ingest.py and returns
    a fully cleaned, typed, and normalized DataFrame.
    """

    @staticmethod
    def clean_data(df: pl.DataFrame) -> pl.DataFrame:
        """
        Main entry point — orchestrates the full transformation pipeline.

        Pipeline order:
            normalize_headers → clean_revenue → parse_dates
            → handle_categories → drop_duplicates

        Args:
            df: Raw Polars DataFrame from DataIngestor.load()

        Returns:
            pl.DataFrame: Cleaned, typed, and normalized DataFrame ready
                          for DuckDB registration in db.py
        """
        if df.is_empty():
            return df

        return (
            df
            .pipe(DataTransformer._normalize_headers)
            .pipe(DataTransformer._clean_revenue)
            .pipe(DataTransformer._parse_dates)
            .pipe(DataTransformer._handle_categories)
            .unique()   # Drop exact duplicate rows — final step
        )

    # ──────────────────────────────────────────────────────────────
    # STEP 1 — Normalize Column Headers
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _normalize_headers(df: pl.DataFrame) -> pl.DataFrame:
        """
        Converts all column names to clean snake_case.

        Rules:
            - Strip leading/trailing whitespace
            - Lowercase all characters
            - Replace spaces with underscores
            - Remove any remaining non-alphanumeric characters (except _)

        Example:
            "Sales Rep Name" → "sales_rep_name"
            "Revenue ($)"    → "revenue_"
        """
        new_cols = {
            col: re.sub(r"[^a-z0-9_]", "", col.lower().strip().replace(" ", "_"))
            for col in df.columns
        }
        return df.rename(new_cols)

    # ──────────────────────────────────────────────────────────────
    # STEP 2 — Clean Revenue Column
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _clean_revenue(df: pl.DataFrame) -> pl.DataFrame:
        """
        Extracts numeric values from currency strings and ensures Float64.

        Handles:
            - Already numeric columns (Int32, Float32, Float64) — cast safely
            - String columns with symbols like "$1,200.00" — strip and cast
            - Null values → filled with 0.0

        Args:
            df: DataFrame post header normalization

        Returns:
            DataFrame with 'revenue' as pl.Float64, nulls filled with 0.0
        """
        if "revenue" not in df.columns:
            return df

        revenue_dtype = df["revenue"].dtype

        if revenue_dtype == pl.Utf8:
            # Strip currency symbols, commas, and whitespace then cast
            df = df.with_columns(
                pl.col("revenue")
                .str.replace_all(r"[\$,\s]", "")
                .cast(pl.Float64, strict=False)
                .fill_null(0.0)
                .alias("revenue")
            )
        elif revenue_dtype in (pl.Int32, pl.Int64, pl.Float32):
            # Safe upcast to Float64 for consistent downstream SQL arithmetic
            df = df.with_columns(
                pl.col("revenue")
                .cast(pl.Float64)
                .fill_null(0.0)
                .alias("revenue")
            )
        else:
            # Already Float64 — just fill nulls
            df = df.with_columns(
                pl.col("revenue").fill_null(0.0)
            )

        return df

    # ──────────────────────────────────────────────────────────────
    # STEP 3 — Parse Date Column
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_dates(df: pl.DataFrame) -> pl.DataFrame:
        """
        Coerces the 'date' column to pl.Date type.

        Handles:
            - Already parsed pl.Date / pl.Datetime — no-op
            - String columns (Utf8) — parse with strict=False
              (unparseable rows become null, then dropped)

        Args:
            df: DataFrame post revenue cleaning

        Returns:
            DataFrame with 'date' as pl.Date, invalid rows dropped
        """
        if "date" not in df.columns:
            return df

        date_dtype = df["date"].dtype

        if date_dtype == pl.Utf8:
            df = df.with_columns(
                pl.col("date")
                .str.to_date(strict=False)   # Failures → null, not exception
                .alias("date")
            )
            # Drop rows where date couldn't be parsed — prevents DuckDB errors
            df = df.filter(pl.col("date").is_not_null())

        elif date_dtype == pl.Datetime:
            # Truncate Datetime → Date (drop time component)
            df = df.with_columns(
                pl.col("date").cast(pl.Date).alias("date")
            )

        # pl.Date — already correct, pass through
        return df

    # ──────────────────────────────────────────────────────────────
    # STEP 4 — Handle Categorical Columns
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _handle_categories(df: pl.DataFrame) -> pl.DataFrame:
        """
        Ensures all required categorical columns exist and have no nulls.

        Required columns: rep, region, product, stage
            - If a column is missing entirely → created with "Unknown"
            - If a column exists → null values filled with "Unknown"

        This prevents KeyErrors and empty charts in views.py when the
        user uploads a CSV that's missing one of these columns.

        Args:
            df: DataFrame post date parsing

        Returns:
            DataFrame with all four categoricals guaranteed to be present
        """
        required_cats = ["rep", "region", "product", "stage"]

        for col in required_cats:
            if col not in df.columns:
                # Column missing entirely — create with placeholder
                df = df.with_columns(
                    pl.lit("Unknown").alias(col)
                )
            else:
                # Column exists — fill any nulls
                df = df.with_columns(
                    pl.col(col).fill_null("Unknown")
                )

        return df
