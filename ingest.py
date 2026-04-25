"""
ingest.py - Data Acquisition Layer for SalesIntelDashboard.
Handles secure file uploads and initial schema validation using Polars.
"""

import polars as pl
import pandas as pd
import streamlit as st
import io
from typing import Union, List

class DataIngestor:
    REQUIRED_COLUMNS = {"date", "revenue", "rep", "region", "product", "stage"}

    @staticmethod
    def load_data(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> pl.DataFrame:
        """
        Loads an uploaded CSV or Excel file into a Polars DataFrame.
        
        Args:
            uploaded_file: The file buffer from Streamlit's st.file_uploader.
            
        Returns:
            pl.DataFrame: The raw, loaded data.
            
        Raises:
            ValueError: If file type is unsupported or required columns are missing.
        """
        if uploaded_file is None:
            return pl.DataFrame()

        file_name = uploaded_file.name.lower()
        
        try:
            # Route based on file extension
            if file_name.endswith('.csv'):
                df = pl.read_csv(io.BytesIO(uploaded_file.getvalue()))
            elif file_name.endswith(('.xls', '.xlsx')):
                # Polars uses fastexcel/xlsx2csv under the hood; 
                # falling back to pandas for Excel is often more stable for messy SMB files
                pdf = pd.read_excel(io.BytesIO(uploaded_file.getvalue()))
                df = pl.from_pandas(pdf)
            else:
                raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

            # Validate basic schema presence
            DataIngestor._validate_schema(df)
            
            return df

        except Exception as e:
            # Log error for developer, raise clean message for UI
            raise ValueError(f"Ingestion Error: {str(e)}")

    @staticmethod
    def _validate_schema(df: pl.DataFrame) -> None:
        """Checks if the minimum required columns exist (case-insensitive check)."""
        current_cols = {col.lower() for col in df.columns}
        missing = DataIngestor.REQUIRED_COLUMNS - current_cols
        
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")

# Usage Example:
# raw_df = DataIngestor.load_data(st.sidebar.file_uploader("Upload CRM Export"))
