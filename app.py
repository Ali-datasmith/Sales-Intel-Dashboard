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
    page_title="Sales Intel Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Apply Custom Styling
apply_custom_theme()

def main():
    st.title("⚡ Sales Intel Terminal")
    
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
        # 4. CLEAN LANDING STATE (Fixes the ghost icon)
        st.warning("Please upload a data file in the sidebar to begin.")
        
        # Using a reliable Unsplash Source with the correct modern parameter
        st.image(
            "https://images.unsplash.com/photo-1551288049-bbbda536339a?q=80&w=2070&auto=format&fit=crop", 
            use_container_width=True
        )

        st.markdown("""
            <div style="text-align: center; padding: 20px; background-color: #1E1E1E; border-radius: 10px; border: 1px solid #333; margin-top: 10px;">
                <h3 style="color: #FFD700; margin: 0;">⚡ Engine Standby</h3>
                <p style="color: #AAAAAA; margin: 10px 0 0 0;">The high-performance analytical core is primed. Please upload a CRM export to generate real-time intelligence.</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
