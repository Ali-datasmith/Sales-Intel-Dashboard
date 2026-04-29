import streamlit as st
from theme import apply_custom_theme
from ingest import DataIngestor
from transform import DataTransformer
from db import db_engine
from filters import SidebarFilters
from views import DashboardViews
from utils import generate_sample_data  # Import our new helper

# 1. Page Configuration
st.set_page_config(
    page_title="Sales Intel Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_theme()

def main():
    st.title("⚡ Sales Intel Terminal")
    
    # --- STEP 2: SAMPLE DATA IN SIDEBAR ---
    with st.sidebar:
        st.markdown("### 📥 Data Ingestion")
        uploaded_file = st.file_uploader("Upload CRM Export", type=["csv", "xlsx"])
        
        sample_csv = generate_sample_data()
        st.download_button(
            label="Get Sample CRM Data",
            data=sample_csv,
            file_name="sample_sales_data.csv",
            mime="text/csv",
            help="Download a template to test the terminal immediately"
        )
    
    if uploaded_file:
        try:
            raw_df = DataIngestor.load_data(uploaded_file)
            clean_df = DataTransformer.clean_data(raw_df)
            db_engine.seed_data(clean_df)
            
            # --- STEP 1: SUCCESS GLOW ---
            st.sidebar.markdown("""
                <div style="padding:10px; border-radius:5px; border:1px solid #00FBFF; background-color:rgba(0,251,255,0.1); color:#00FBFF; text-align:center;">
                    ⚡ ENGINE PRIMED & READY
                </div>
            """, unsafe_allow_html=True)
            
            filter_state = SidebarFilters.render(clean_df)
            page = st.sidebar.radio("Navigation", ["Overview", "Regional Breakdown", "Funnel Analysis", "Rep Performance"])
            
            st.divider()
            
            if page == "Overview":
                DashboardViews.show_overview()
            # ... (rest of your routing)
            
        except Exception as e:
            st.error(f"Application Error: {e}")
    else:
        # --- STEP 3: METRIC SKELETONS ---
        col1, col2, col3 = st.columns(3)
        for col in [col1, col2, col3]:
            col.markdown("""
                <div style="background-color:#161616; padding:20px; border-radius:10px; border:1px solid #222; text-align:center; color:#444;">
                    <small>AWAITING DATA</small><br><b style="font-size:1.5em;">$ 0.00</b>
                </div>
            """, unsafe_allow_html=True)

        # --- YOUR BEAUTIFUL NEON HERO SECTION ---
        st.markdown("""
            <div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); padding: 60px; border-radius: 20px; border: 1px solid #333; text-align: center; margin-top: 20px; box-shadow: 0px 10px 40px rgba(0, 251, 255, 0.1);">
                <h1 style="color: #FFD700; font-size: 3.5em; margin-bottom: 15px; filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.4));">⚡</h1>
                <h2 style="color: #00FBFF; font-family: 'Segoe UI', sans-serif; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;">Terminal Ready for Ingestion</h2>
                <p style="color: #999; font-size: 1.2em; max-width: 600px; margin: 0 auto; line-height: 1.6;">The analytical core is standing by. Upload data to unlock <span style="color: #00FBFF;">real-time intelligence</span>.</p>
                <div style="margin-top: 40px; height: 3px; background: linear-gradient(90deg, transparent, #00FBFF, transparent); width: 60%; margin-left: 20%; box-shadow: 0 0 10px #00FBFF;"></div>
            </div>
        """, unsafe_allow_html=True)

        # --- STEP 4: BRANDING FOOTER ---
        st.markdown(f"""
            <div style="text-align: center; color: #444; margin-top: 50px; font-size: 0.8em;">
                Developed by <span style="color: #00FBFF;">Ali-datasmith</span> | High-Velocity Sales Analytics ⚡
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
