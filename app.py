import streamlit as st
from theme import apply_custom_theme
from ingest import DataIngestor
from transform import DataTransformer
from db import db_engine
from filters import SidebarFilters
from views import DashboardViews
from utils import generate_sample_data 

st.set_page_config(page_title="Sales Intel Terminal", page_icon="⚡", layout="wide")

# --- COMPLETE THEME & ANIMATION ENGINE ---
st.markdown("""
<style>
    /* Global Styles */
    h1, h2, h3, h4 { color: #00FBFF !important; font-family: 'Courier New', monospace; }
    
    /* Typewriter Effect */
    .typewriter h2 {
      overflow: hidden;
      border-right: .15em solid #00FBFF;
      white-space: nowrap;
      margin: 0 auto;
      letter-spacing: .12em;
      animation: typing 3s steps(30, end), blink-caret .75s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #00FBFF; } }

    /* Cyan Fix for Multiselect & Tabs */
    span[data-baseweb="tag"] { background-color: rgba(0, 251, 255, 0.1) !important; color: #00FBFF !important; border: 1px solid #00FBFF !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #00FBFF !important; border-bottom-color: #00FBFF !important; }
    div[data-baseweb="tab-highlight"] { background-color: #00FBFF !important; }

    /* Status Badge & Sidebar */
    .status-badge { padding: 5px 12px; border-radius: 20px; font-size: 0.75em; border: 1px solid #00FBFF; color: #00FBFF; display: inline-block; margin-bottom: 15px; }
    .pulse { animation: pulse-status 2s infinite; }
    @keyframes pulse-status { 0% { box-shadow: 0 0 0 0px rgba(0, 251, 255, 0.4); } 70% { box-shadow: 0 0 0 8px rgba(0, 251, 255, 0); } 100% { box-shadow: 0 0 0 0px rgba(0, 251, 255, 0); } }
    [data-testid="stSidebar"] { border-right: 1px solid #00FBFF !important; }
</style>
""", unsafe_allow_html=True)

apply_custom_theme()

def main():
    st.title("⚡ Sales Intel Terminal")

    with st.sidebar:
        if 'data_processed' not in st.session_state:
            st.markdown('<div class="status-badge" style="color:#888; border-color:#444;">⚪ SYSTEM IDLE</div>', unsafe_allow_html=True)
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

            filter_state = SidebarFilters.render(clean_df)
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🗺️ Regional", "🌪️ Funnel", "👤 Reps"])
            with tab1: DashboardViews.show_overview()
            with tab2: DashboardViews.show_regional_breakdown()
            with tab3: DashboardViews.show_funnel_analysis()
            with tab4: DashboardViews.show_rep_performance()

        except Exception as e:
            # --- UPDATED ERROR HANDLING ---
            st.error(f"⚠️ **Invalid File Format:** {e}")
            st.info("💡 **Tip:** Please ensure your CSV has all required columns. You can download the **'Sample CRM Data'** from the sidebar for reference.")
            st.stop() 
    else:
        # Landing Page Content
        st.markdown('<div class="typewriter"><h2>Ready to Generate Insights</h2></div>', unsafe_allow_html=True)
        st.markdown('<div style="background:rgba(10,10,10,0.4); padding:30px; border-radius:15px; border:1px solid #222; text-align:center; margin:20px 0;">Terminal awaiting CRM data stream via Sidebar.</div>', unsafe_allow_html=True)

        # 3 Points Guide
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### 📥 Ingest")
            st.caption("Upload your raw sales CSV/Excel.")
        with c2:
            st.markdown("#### ⚙️ Process")
            st.caption("Polars engine optimizes data instantly.")
        with c3:
            st.markdown("#### 📈 Analyze")
            st.caption("Explore interactive terminal views.")

    # Footer
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #444; font-size: 0.8em;">Developed by Muhammad Ali Rajput | High-Performance Data Terminal</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align: center; color: #888; font-size: 0.85em; letter-spacing: 0.1em; font-family: 'Courier New', monospace;">
        <span style="color: #444;">//</span> 
        <span style="color: #00FBFF; font-weight: bold;">ARCHITECTED BY</span> 
        <span style="color: white; font-weight: bold;">Ali-datasmith</span> 
        <span style="color: #444;">//</span> 
        <span style="color: #888;">HIGH-PERFORMANCE DATA TERMINAL v1.0</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
