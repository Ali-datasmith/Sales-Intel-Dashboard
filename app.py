import streamlit as st
from theme import apply_custom_theme
from ingest import DataIngestor
from transform import DataTransformer
from db import db_engine
from filters import SidebarFilters
from views import DashboardViews
from utils import generate_sample_data 
from reports import PDFReport  # Importing the new report tool

st.set_page_config(
    page_title="Sales Intel Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_custom_theme()

def main():
    st.sidebar.markdown("""
        <div style="padding: 10px; border-bottom: 1px solid #333; margin-bottom: 20px;">
            <h2 style="color: #00FBFF; margin: 0;">⚡ INTEL</h2>
            <small style="color: #666;">COMMAND OPERATING SYSTEM</small>
        </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 📥 DATA UPLINK")
        uploaded_file = st.sidebar.file_uploader("Upload CRM Export", type=["csv", "xlsx"])
        
        sample_csv = generate_sample_data()
        st.download_button("GET SYSTEM TEMPLATE", data=sample_csv, file_name="template.csv")
    
    if uploaded_file:
        try:
            raw_df = DataIngestor.load_data(uploaded_file)
            clean_df = DataTransformer.clean_data(raw_df)
            db_engine.seed_data(clean_df)
            
            # PDF EXPORT BUTTON IN SIDEBAR
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 📄 EXPORT PROTOCOL")
            report_gen = PDFReport(clean_df)
            pdf_bytes = report_gen.generate()
            
            st.sidebar.download_button(
                label="⚡ DOWNLOAD PDF REPORT",
                data=pdf_bytes,
                file_name="Sales_Intel_Report.pdf",
                mime="application/pdf"
            )
            
            filter_state = SidebarFilters.render(clean_df)
            page = st.sidebar.radio("Navigation", ["Overview", "Regional Breakdown", "Funnel Analysis", "Rep Performance"])
            
            if page == "Overview":
                DashboardViews.show_overview()
            elif page == "Regional Breakdown":
                DashboardViews.show_regional_breakdown()
            # Add other pages as needed...
            
        except Exception as e:
            st.error(f"SYSTEM ERROR: {e}")
    else:
        # AESTHETIC LANDING
        st.markdown("""
            <div style="margin-top: 40px; padding: 80px; border: 1px solid #1a1a1a; background: rgba(10,10,12,0.9); position: relative; text-align: left; font-family: monospace;">
                <div style="color: #00FBFF; margin-bottom: 10px;">> SYSTEM STATUS: <span style="color: #FFD700;">AWAITING_INPUT</span></div>
                <h1 style="color: white; font-size: 3em; margin: 0; letter-spacing: -2px;">Initialize Analytics.</h1>
                <p style="color: #888; font-size: 1.2em; margin-bottom: 40px;">Drop your CRM data into the uplink to decrypt sales performance.</p>
                <div style="display: inline-block; padding: 10px 20px; border: 1px solid #333; color: #666; font-size: 0.8em;">READY FOR INGESTION_</div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
