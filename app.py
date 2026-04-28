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
        # --- NEON CYAN HERO SECTION ---
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
                padding: 60px;
                border-radius: 20px;
                border: 1px solid #333;
                text-align: center;
                margin-top: 20px;
                box-shadow: 0px 10px 40px rgba(0, 251, 255, 0.1);
            ">
                <h1 style="color: #FFD700; font-size: 3.5em; margin-bottom: 15px; filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.4));">⚡</h1>
                <h2 style="color: #00FBFF; font-family: 'Segoe UI', sans-serif; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;">
                    Terminal Ready for Ingestion
                </h2>
                <p style="color: #999; font-size: 1.2em; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                    The high-performance analytical core is primed and standing by. 
                    Upload your CRM data in the sidebar to unlock <span style="color: #00FBFF;">real-time sales intelligence</span>.
                </p>
                <div style="margin-top: 40px; height: 3px; background: linear-gradient(90deg, transparent, #00FBFF, transparent); width: 60%; margin-left: 20%; box-shadow: 0 0 10px #00FBFF;"></div>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
