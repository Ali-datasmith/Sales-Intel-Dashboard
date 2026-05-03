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

# --- THE ULTIMATE CYAN THEME FIX ---
st.markdown("""
<style>
    /* 1. Global Text & Scrollbar */
    h1, h2, h3, h4 { color: #00FBFF !important; font-family: 'Courier New', monospace; }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #00FBFF; border-radius: 10px; }

    /* 2. Fix for Red Tabs (Active Tab Indicator) */
    button[data-baseweb="tab"] { color: white !important; }
    button[data-baseweb="tab"][aria-selected="true"] { 
        color: #00FBFF !important; 
        border-bottom-color: #00FBFF !important; 
    }
    div[data-baseweb="tab-highlight"] { background-color: #00FBFF !important; }

    /* 3. Fix for Red Multiselect Badges (Tags) */
    span[data-baseweb="tag"] {
        background-color: rgba(0, 251, 255, 0.1) !important;
        color: #00FBFF !important;
        border: 1px solid #00FBFF !important;
    }
    span[data-baseweb="tag"] svg { fill: #00FBFF !important; }

    /* 4. Status Badge & Pulse */
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: bold;
        border: 1px solid #00FBFF !important;
        background-color: rgba(0, 251, 255, 0.05) !important;
        color: #00FBFF !important;
        display: inline-block;
        margin-bottom: 15px;
    }
    .pulse { animation: pulse-status 2s infinite; }
    @keyframes pulse-status {
        0% { box-shadow: 0 0 0 0px rgba(0, 251, 255, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(0, 251, 255, 0); }
        100% { box-shadow: 0 0 0 0px rgba(0, 251, 255, 0); }
    }

    /* 5. Sidebar & File Uploader */
    [data-testid="stSidebar"] { border-right: 2px solid #00FBFF !important; }
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #00FBFF !important;
        background: rgba(0, 251, 255, 0.05) !important;
    }
    [data-testid="stFileUploadDropzone"]:hover { box-shadow: 0 0 20px #00FBFF; }

    /* 6. Metrics & General UI */
    [data-testid="stMetric"] { border-left: 2px solid #00FBFF; padding-left: 10px; }
</style>
""", unsafe_allow_html=True)

apply_custom_theme()

def main():
    st.title("⚡ Sales Intel Terminal")

    with st.sidebar:
        if 'data_processed' not in st.session_state:
            st.markdown('<div class="status-badge" style="color:#888 !important; border-color:#444 !important;">⚪ SYSTEM IDLE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge pulse">🟢 POLARS ACTIVE</div>', unsafe_allow_html=True)

        st.markdown("### 📥 Data Ingestion")
        uploaded_file = st.sidebar.file_uploader("Upload CRM Export", type=["csv", "xlsx"])
        sample_csv = generate_sample_data()
        st.download_button(label="Get Sample CRM Data", data=sample_csv, file_name="sample.csv", mime="text/csv")

    if uploaded_file:
        try:
            raw_df = DataIngestor.load_data(uploaded_file)
            clean_df = DataTransformer.clean_data(raw_df)
            db_engine.seed_data(clean_df)
            st.session_state['data_processed'] = True

            st.sidebar.markdown('<div style="padding:10px; border-radius:5px; border:1px solid #00FBFF; background-color:rgba(0,251,255,0.1); color:#00FBFF; text-align:center; font-weight:bold;">⚡ ENGINE PRIMED</div>', unsafe_allow_html=True)

            filter_state = SidebarFilters.render(clean_df)
            
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🗺️ Regional", "🌪️ Funnel", "👤 Reps"])
            with tab1: DashboardViews.show_overview()
            with tab2: DashboardViews.show_regional_breakdown()
            with tab3: DashboardViews.show_funnel_analysis()
            with tab4: DashboardViews.show_rep_performance()

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        # Typewriter Landing Page
        st.markdown('<div class="typewriter"><h2>Ready to Generate Insights</h2></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(10,10,10,0.4); padding: 40px; border-radius: 15px; border: 1px solid #222; text-align: center; margin-top: 20px;">
            <p style="color: #888; font-size: 1.2em;">Terminal awaiting CRM data stream via Sidebar.</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
