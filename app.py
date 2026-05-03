import streamlit as st
from reports import PDFReport
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

# --- THE STUNNING MARKDOWN BLOCK ---
st.markdown("""
<style>
    /* 1. Headings Cyan */
    h1, h2, h3, h4, h5, h6 { color: #00FBFF !important; }

    /* 2. Sidebar Border & Tags (Red to Cyan) */
    [data-testid="stSidebar"] { border-right: 2px solid #00FBFF !important; }
    [data-baseweb="tag"] { background-color: #00FBFF !important; color: #000 !important; }

    /* 3. File Uploader Glow Effect */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #00FBFF !important;
        background: rgba(0, 251, 255, 0.05) !important;
        transition: all 0.3s ease-in-out;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        box-shadow: 0 0 15px #00FBFF;
    }

    /* 4. Engine Primed Pulse Animation */
    div[style*="background-color:rgba(0,251,255,0.1)"] {
        animation: pulse-animation 2s infinite;
    }
    @keyframes pulse-animation {
        0% { box-shadow: 0 0 0 0px rgba(0, 251, 255, 0.7); }
        100% { box-shadow: 0 0 0 10px rgba(0, 251, 255, 0); }
    }

    /* 5. Metric Cards Fade-Slide-Up Animation */
    [data-testid="stMetric"], div[style*="background-color:#161616"] {
        animation: fadeSlideUp 0.8s ease-out forwards;
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* 6. DataFrame Border Scan Animation */
    .stDataFrame {
        border: 1px solid #333 !important;
        position: relative;
    }
    .stDataFrame::before {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 2px;
        background: #00FBFF; animation: scanLine 3s linear infinite;
    }
    @keyframes scanLine { 0% { top: 0%; } 100% { top: 100%; } }

    /* 7. Loading Spinner Cyan */
    [data-testid="stLoadingIcon"] svg { fill: #00FBFF !important; }

    /* 8. Custom Cyan Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0e1117; }
    ::-webkit-scrollbar-thumb { background: #00FBFF; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

apply_custom_theme()

def main():
    st.title("⚡ Sales Intel Terminal")

    with st.sidebar:
        st.markdown("### 📥 Data Ingestion")
        uploaded_file = st.sidebar.file_uploader("Upload CRM Export", type=["csv", "xlsx"])

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

            st.sidebar.markdown("""
                <div style="padding:10px; border-radius:5px; border:1px solid #00FBFF; background-color:rgba(0,251,255,0.1); color:#00FBFF; text-align:center; font-weight:bold;">
                    ⚡ ENGINE PRIMED & READY
                </div>
            """, unsafe_allow_html=True)

            filter_state = SidebarFilters.render(clean_df)
            page = st.sidebar.radio("Navigation", ["Overview", "Regional Breakdown", "Funnel Analysis", "Rep Performance"])

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
    else:
        col1, col2, col3 = st.columns(3)
        for col in [col1, col2, col3]:
            col.markdown('<div style="background-color:#161616; padding:20px; border-radius:10px; border:1px solid #222; text-align:center; color:#444;"><small>AWAITING DATA</small><br><b style="font-size:1.5em;">$ 0.00</b></div>', unsafe_allow_html=True)

        st.markdown("""
<div style="background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%); padding: 60px; border-radius: 20px; border: 1px solid #333; text-align: center; margin-top: 20px; box-shadow: 0px 10px 40px rgba(0, 251, 255, 0.1);">
    <h1 style="color: #FFD700; font-size: 3.5em; margin-bottom: 15px; filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.4));">⚡</h1>
    <h2 style="color: #00FBFF; font-family: 'Segoe UI', sans-serif; font-weight: 800; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 2px;">
        Ready to Generate Insights
    </h2>
    <p style="color: #999; font-size: 1.2em; max-width: 600px; margin: 0 auto; line-height: 1.6;">
        Please upload your CRM data in the sidebar to begin your 
        <span style="color: #00FBFF; font-weight: bold;">real-time sales analysis</span>.
    </p>
    <div style="margin-top: 40px; height: 3px; background: linear-gradient(90deg, transparent, #00FBFF, transparent); width: 60%; margin-left: 20%; box-shadow: 0 0 10px #00FBFF;"></div>
</div>
<div style="text-align: center; color: #444; margin-top: 50px; font-size: 0.8em;">
    Developed by <span style="color: #00FBFF;">Ali-datasmith</span> | High-Velocity Polars Engine ⚡
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
