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
            raw_df = DataIngestor.load_data(uploaded_file)
            clean_df = DataTransformer.clean_data(raw_df)
            db_engine.seed_data(clean_df)
            filter_state = SidebarFilters.render(clean_df)
            
            page = st.sidebar.radio(
                "Navigation", 
                ["Overview", "Regional Breakdown", "Funnel Analysis", "Rep Performance"]
            )
            
            st.divider()
            
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
        # --- THE ABSOLUTE FIX ---
        # We REMOVED st.image entirely to kill the broken icon bug.
        # Instead, we use a high-end CSS Hero Component.
        
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1e1e1e 0%, #121212 100%);
                padding: 60px;
                border-radius: 20px;
                border: 1px solid #333;
                text-align: center;
                margin-top: 20px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
            ">
                <h1 style="color: #FFD700; font-size: 3em; margin-bottom: 10px;">⚡</h1>
                <h2 style="color: #ffffff; font-family: sans-serif; font-weight: 700; margin-bottom: 20px;">
                    Terminal Ready for Ingestion
                </h2>
                <p style="color: #888; font-size: 1.2em; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                    The high-performance analytical core is primed and standing by. 
                    Upload your CRM data in the sidebar to unlock real-time sales intelligence.
                </p>
                <div style="margin-top: 30px; height: 2px; background: linear-gradient(90deg, transparent, #FFD700, transparent); width: 50%; margin-left: 25%;"></div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
