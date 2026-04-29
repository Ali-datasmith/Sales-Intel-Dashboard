import streamlit as st
from theme import apply_custom_theme
from ingest import DataIngestor
from transform import DataTransformer
from db import db_engine
from filters import SidebarFilters
from views import DashboardViews
from utils import generate_sample_data 

st.set_page_config(
    page_title="Sales Intel Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global CSS for Glassmorphism and Button Hover Effects
st.markdown("""
<style>
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 25, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0, 251, 255, 0.1);
    }
    
    /* Custom Upload Button Glow */
    div.stButton > button:first-child {
        background-color: transparent;
        border: 1px solid #00FBFF;
        color: #00FBFF;
        box-shadow: 0 0 10px rgba(0, 251, 255, 0.2);
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:hover {
        background-color: #00FBFF;
        color: #000;
        box-shadow: 0 0 20px #00FBFF;
    }

    /* Success Glow Animation */
    @keyframes pulse {
        0% { box-shadow: 0 0 5px #00FBFF; }
        50% { box-shadow: 0 0 20px #00FBFF; }
        100% { box-shadow: 0 0 5px #00FBFF; }
    }
</style>
""", unsafe_allow_html=True)

apply_custom_theme()

def main():
    # --- LOGO PLACEMENT ---
    # Replace 'YOUR_LOGO_URL' with your actual logo link or use the ⚡ icon as a placeholder
    st.sidebar.markdown("""
        <div style="text-align: center; padding-bottom: 20px;">
            <h1 style="color: #00FBFF; font-size: 2.5em; text-shadow: 0 0 10px #00FBFF;">⚡</h1>
            <p style="color: #666; font-size: 0.7em; letter-spacing: 3px;">ALI-DATASMITH v3.0</p>
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 📥 Data Ingestion")
        uploaded_file = st.sidebar.file_uploader("Upload CRM Export", type=["csv", "xlsx"])
        
        sample_csv = generate_sample_data()
        st.download_button(
            label="Get Sample CRM Data",
            data=sample_csv,
            file_name="sample_sales_data.csv",
            mime="text/csv"
        )
    
    if uploaded_file:
        try:
            raw_df = DataIngestor.load_data(uploaded_file)
            clean_df = DataTransformer.clean_data(raw_df)
            db_engine.seed_data(clean_df)
            
            st.sidebar.markdown("""
                <div style="padding:10px; border-radius:5px; border:1px solid #00FBFF; background-color:rgba(0,251,255,0.1); color:#00FBFF; text-align:center; font-weight:bold; animation: pulse 2s infinite;">
                    ⚡ ENGINE ACTIVE
                </div>
            """, unsafe_allow_html=True)
            
            filter_state = SidebarFilters.render(clean_df)
            page = st.sidebar.radio("Navigation", ["Overview", "Regional Breakdown", "Funnel Analysis", "Rep Performance"])
            
            if page == "Overview":
                DashboardViews.show_overview()
            # ... other routes
            
        except Exception as e:
            st.error(f"Application Error: {e}")
    else:
        # AESTHETIC METRIC SKELETONS
        col1, col2, col3 = st.columns(3)
        for col in [col1, col2, col3]:
            col.markdown('<div style="background-color:rgba(30,30,35,0.5); padding:20px; border-radius:15px; border:1px solid #222; text-align:center; color:#444;"><small style="letter-spacing:2px;">AWAITING SIGNAL</small><br><b style="font-size:1.8em; color:#222;">$ --,---</b></div>', unsafe_allow_html=True)

        # UPDATED HERO CARD
        st.markdown("""
<div style="background: radial-gradient(circle at top left, #1a1a1a, #050505); padding: 80px; border-radius: 25px; border: 1px solid rgba(255, 215, 0, 0.1); text-align: center; margin-top: 30px; box-shadow: 0px 20px 50px rgba(0, 0, 0, 0.5);">
    <div style="font-size: 4em; margin-bottom: 20px; filter: drop-shadow(0 0 15px #FFD700);">⚡</div>
    <h1 style="color: #FFF; font-family: 'Segoe UI', sans-serif; font-weight: 900; margin-bottom: 10px; letter-spacing: -1px;">
        Analytics <span style="color: #00FBFF;">Terminal</span>
    </h1>
    <h3 style="color: #00FBFF; font-family: 'Segoe UI', sans-serif; font-weight: 300; margin-bottom: 30px; text-transform: uppercase; letter-spacing: 4px; font-size: 0.9em; opacity: 0.8;">
        Ready for Ingestion
    </h3>
    <p style="color: #777; font-size: 1.1em; max-width: 500px; margin: 0 auto; line-height: 1.8;">
        Establish a data connection via the sidebar to populate your 
        <span style="color: #FFD700; font-weight: bold;">intelligence dashboard</span>.
    </p>
    <div style="margin-top: 50px; height: 1px; background: linear-gradient(90deg, transparent, rgba(0, 251, 255, 0.5), transparent); width: 80%; margin-left: 10%;"></div>
</div>
<div style="text-align: center; color: #333; margin-top: 60px; font-size: 0.7em; letter-spacing: 2px; text-transform: uppercase;">
    Secure Pipeline • High-Velocity Engine • <span style="color: #00FBFF;">Ali-datasmith</span>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
