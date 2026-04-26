"""
app.py - The Main Entry Point.
Coordinates data flow between ingestion, transformation, and visualization.
"""

import streamlit as st
from theme import apply_custom_theme
from ingest import DataIngestor
from transform import DataTransformer
from db import db_engine
from filters import SidebarFilters
from views import DashboardViews

# 1. Page Configuration
st.set_page_config(
    page_title="Sales Intel Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Apply Custom Styling
apply_custom_theme()

def main():
    st.title("🛡️ Sales Intel Dashboard")
    
    # 3. Data Ingestion Section
    uploaded_file = st.sidebar.file_uploader("Upload CRM Export (CSV/Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            # Step A: Ingest & Transform
            raw_df = DataIngestor.load_data(uploaded_file)
            clean_df = DataTransformer.clean_data(raw_df)
            
            # Step B: Seed Database Engine
            db_engine.seed_data(clean_df)
            
            # Step C: Global Filters
            filter_state = SidebarFilters.render(clean_df)
            
            # Step D: Navigation & Routing
            page = st.sidebar.radio(
                "Navigation", 
                ["Overview", "Regional Breakdown", "Funnel Analysis", "Rep Performance"]
            )
            
            st.divider()
            
            # Routing Logic
            if page == "Overview":
                DashboardViews.show_overview()
            elif page == "Regional Breakdown":
                DashboardViews.show_regional_breakdown()
            elif page == "Funnel Analysis":
                DashboardViews.show_funnel_analysis()
            elif page == "Rep Performance":
                DashboardViews.show_rep_performance()

        except Exception as e:
            st.error(f"Application Error: {e}")
            st.info("Please ensure your file contains: Date, Revenue, Rep, Region, Product, Stage")
    else:
        st.warning("Please upload a data file in the sidebar to begin.")
        st.image("https://via.placeholder.com/800x400?text=Awaiting+Data+Upload", use_column_width=True)

if __name__ == "__main__":
    main()
