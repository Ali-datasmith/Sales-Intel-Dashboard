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

# --- THE AGGRESSIVE UI INJECTION ---
st.markdown("""
<style>
    /* 1. Headings & Scrollbar */
    h1, h2, h3 { color: #00FBFF !important; }
    ::-webkit-scrollbar { width: 10px !important; }
    ::-webkit-scrollbar-thumb { background: #00FBFF !important; border-radius: 10px !important; box-shadow: 0 0 10px #00FBFF !important; }

    /* 2. File Uploader Glow (Force Hover) */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #00FBFF !important;
        background: rgba(0, 251, 255, 0.05) !important;
        transition: 0.4s all ease-in-out !important;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        box-shadow: 0 0 30px rgba(0, 251, 255, 0.6) !important;
        border-style: solid !important;
    }

    /* 3. Engine Primed Pulse Animation (Global Target) */
    div[style*="background-color:rgba(0,251,255,0.1)"], .element-container:has(div[style*="color:#00FBFF"]) {
        animation: pulse-glow 2s infinite !important;
    }
    @keyframes pulse-glow {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 251, 255, 0.7); }
        70% { transform: scale(1.02); box-shadow: 0 0 0 15px rgba(0, 251, 255, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(0, 251, 255, 0); }
    }

    /* 4. Metric Cards Fade-Slide-Up (Force Animation) */
    [data-testid="stMetric"], .stMetricValue, div[style*="background-color:#161616"] {
        animation: slideIn 1s ease-out forwards !important;
        opacity: 0;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(50px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 5. DataFrame Border Scan (Visual Trick) */
    .stDataFrame {
        border-top: 2px solid #00FBFF !important;
        position: relative !important;
    }
    .stDataFrame::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 4px;
        background: linear-gradient(90deg, transparent, #00FBFF, transparent);
        animation: scanner 3s linear infinite !important;
    }
    @keyframes scanner { 0% { left: -100%; } 100% { left: 100%; } }

    /* 6. Loading Spinner Cyan */
    [data-testid="stLoadingIcon"] svg { fill: #00FBFF !important; stroke: #00FBFF !important; }
</style>
""", unsafe_allow_html=True)

apply_custom_theme()

def main():
    st.title("⚡ Sales Intel Terminal")

    with st.sidebar:
        st.markdown("### 📥 Data Ingestion")
        uploaded_file = st.sidebar.file_uploader("Upload CRM Export", type=["csv", "xlsx"])
        sample_csv = generate_sample_data()
        st.download_button(label="Get Sample Data", data=sample_csv, file_name="sample.csv", mime="text/csv")

    if uploaded_file:
        try:
            raw_df = DataIngestor.load_data(uploaded_file)
            clean_df = DataTransformer.clean_data(raw_df)
            db_engine.seed_data(clean_df)

            st.sidebar.markdown('<div style="padding:15px; border-radius:10px; border:2px solid #00FBFF; background-color:rgba(0,251,255,0.1); color:#00FBFF; text-align:center; font-weight:bold;">⚡ ENGINE PRIMED & READY</div>', unsafe_allow_html=True)

            filter_state = SidebarFilters.render(clean_df)
            page = st.sidebar.radio("Navigation", ["Overview", "Regional Breakdown", "Funnel Analysis", "Rep Performance"])

            if page == "Overview": DashboardViews.show_overview()
            elif page == "Regional Breakdown": DashboardViews.show_regional_breakdown()
            elif page == "Funnel Analysis": DashboardViews.show_funnel_analysis()
            elif page == "Rep Performance": DashboardViews.show_rep_performance()

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.markdown('<div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); padding: 60px; border-radius: 20px; border: 1px solid #333; text-align: center; margin-top: 20px;"><h1 style="color: #FFD700; font-size: 3.5em;">⚡</h1><h2 style="color: #00FBFF;">Awaiting Data Ingestion</h2><p style="color: #999;">Upload a file to trigger the high-performance Polars engine.</p></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
