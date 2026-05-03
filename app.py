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

# --- ENHANCED STYLING BLOCK ---
st.markdown("""
<style>
    /* Base Colors & Scrollbar */
    h1, h2, h3, h4 { color: #00FBFF !important; font-family: 'Courier New', monospace; }
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-thumb { background: #00FBFF; border-radius: 10px; }

    /* Typewriter Effect */
    .typewriter h2 {
      overflow: hidden;
      border-right: .15em solid #00FBFF;
      white-space: nowrap;
      margin: 0 auto;
      letter-spacing: .15em;
      animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #00FBFF; } }

    /* Status Badge */
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75em;
        font-weight: bold;
        border: 1px solid #00FBFF;
        display: inline-block;
        margin-bottom: 15px;
    }
    .pulse { animation: pulse-status 2s infinite; }
    @keyframes pulse-status {
        0% { box-shadow: 0 0 0 0px rgba(0, 251, 255, 0.4); }
        70% { box-shadow: 0 0 0 8px rgba(0, 251, 255, 0); }
        100% { box-shadow: 0 0 0 0px rgba(0, 251, 255, 0); }
    }

    /* Original Glow & Sidebar */
    [data-testid="stSidebar"] { border-right: 2px solid #00FBFF !important; }
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #00FBFF !important;
        background: rgba(0, 251, 255, 0.05) !important;
        transition: 0.3s all ease;
    }
    [data-testid="stFileUploadDropzone"]:hover { box-shadow: 0 0 20px #00FBFF; }
</style>
""", unsafe_allow_html=True)

apply_custom_theme()

def main():
    st.title("⚡ Sales Intel Terminal")

    with st.sidebar:
        if 'data_processed' not in st.session_state:
            st.markdown('<div class="status-badge" style="color:#888; border-color:#444;">⚪ SYSTEM IDLE</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge pulse" style="color:#00FBFF;">🟢 POLARS ACTIVE</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="typewriter"><h2>Ready to Generate Insights</h2></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(10,10,10,0.4); padding: 40px; border-radius: 15px; border: 1px solid #222; text-align: center; margin-top: 20px;">
            <p style="color: #888; font-size: 1.2em;">Terminal awaiting CRM data stream via Sidebar.</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### 1. Ingest")
            st.caption("Upload your raw sales CSV or Excel export.")
        with c2:
            st.markdown("#### 2. Process")
            st.caption("Polars engine cleans and transforms data instantly.")
        with c3:
            st.markdown("#### 3. Analyze")
            st.caption("Gain deep insights through interactive visual views.")

if __name__ == "__main__":
    main()
