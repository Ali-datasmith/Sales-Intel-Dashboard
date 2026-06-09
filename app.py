"""
app.py - Entry Point for Sales Intel Terminal.

Responsibilities:
    1. Page config (called ONCE)
    2. CSS / theme injection
    3. Login gate — blocks dashboard until authenticated
    4. Sidebar — file upload + sample data download
    5. Data pipeline — ingest → transform → seed DuckDB
    6. Dashboard routing — 4 tabbed views
    7. Landing page — shown when no data is loaded
    8. Footer
"""

import streamlit as st

from theme import inject_css, section_header, status_badge
from ingest import DataIngestor
from transform import DataTransformer
from db import db_engine
from filters import SidebarFilters
from views import DashboardViews
from utils import generate_sample_data
from login import render_login, render_logout_button

# ══════════════════════════════════════════════════════════════════
# PAGE CONFIG — called ONCE, before any other st.* call
# ══════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title = "Sales Intel Terminal",
    page_icon  = "📊",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)

# Inject glass-morphism CSS + Emerald/Gold palette
inject_css()


# ══════════════════════════════════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════════════════════════════════

if not st.session_state.get("authenticated", False):
    render_login()
    st.stop()   # Block everything below until login succeeds


# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════

def build_sidebar() -> object:
    """
    Renders the sidebar with:
    - User info + logout button
    - Status badge (idle vs active)
    - File uploader
    - Sample data download

    Returns:
        uploaded_file object or None
    """
    with st.sidebar:

        # ── User info + logout ──
        username = st.session_state.get("username", "User")
        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                padding:0.6rem 0 1rem 0;
                border-bottom:1px solid rgba(5,150,105,0.25);
                margin-bottom:1rem;
            ">
                <div>
                    <div style="
                        color:#F1F5F9;
                        font-size:0.85rem;
                        font-weight:600;
                        font-family:Inter,sans-serif;
                    ">👤 {username}</div>
                    <div style="
                        color:#64748B;
                        font-size:0.72rem;
                        font-family:Inter,sans-serif;
                        margin-top:2px;
                    ">Authenticated</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        render_logout_button()

        st.markdown("<br>", unsafe_allow_html=True)

        # ── System status badge ──
        is_active = st.session_state.get("data_processed", False)
        if is_active:
            st.markdown(
                status_badge("● DATA LOADED", "success"),
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                status_badge("○ AWAITING DATA", "default"),
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Data ingestion ──
        st.markdown(
            """
            <div style="
                font-size:0.72rem;
                letter-spacing:0.1em;
                text-transform:uppercase;
                color:#059669;
                font-weight:600;
                font-family:Inter,sans-serif;
                padding-bottom:0.5rem;
                border-bottom:1px solid rgba(5,150,105,0.2);
                margin-bottom:0.75rem;
            ">📥 Data Ingestion</div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Upload your CRM export (CSV or Excel)")
        uploaded_file = st.file_uploader(
            label="CRM Data Upload",
            type=["csv", "xlsx"],
            label_visibility="collapsed"
        )
        st.caption("Max 200 MB · CSV · XLSX")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Sample data download ──
        sample_csv = generate_sample_data()
        st.download_button(
            label="⬇ Download Sample CRM Data",
            data=sample_csv,
            file_name="sample_crm_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    return uploaded_file


# ══════════════════════════════════════════════════════════════════
# LANDING PAGE — shown when no data is loaded
# ══════════════════════════════════════════════════════════════════

def render_landing() -> None:
    """Renders the welcome/hero screen when no file has been uploaded."""

    # ── Hero header ──
    st.markdown(
        """
        <div style="padding:2rem 0 1.5rem 0;">
            <div style="
                font-size:0.75rem;
                letter-spacing:0.18em;
                text-transform:uppercase;
                color:#059669;
                font-weight:600;
                font-family:Inter,sans-serif;
                margin-bottom:0.75rem;
            ">High-Performance Sales Analytics</div>
            <h1 style="
                font-size:clamp(2.4rem,5vw,4rem);
                font-weight:800;
                letter-spacing:-0.03em;
                line-height:1.05;
                color:#F1F5F9;
                font-family:Inter,sans-serif;
                margin:0 0 0.5rem 0;
            ">Sales Intel <span style="color:#059669;">Terminal</span></h1>
            <p style="
                font-size:1rem;
                color:#94A3B8;
                font-family:Inter,sans-serif;
                margin:0.75rem 0 0 0;
                max-width:520px;
                line-height:1.6;
            ">
                Upload your CRM export from the sidebar to generate
                instant revenue insights, pipeline analysis, and rep performance dashboards.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Waiting state card ──
    st.markdown(
        """
        <div class="glass-card" style="text-align:center;padding:2rem;margin:1rem 0 2rem 0;">
            <div style="font-size:2.5rem;margin-bottom:0.75rem;">📂</div>
            <div style="
                color:#94A3B8;
                font-family:Inter,sans-serif;
                font-size:0.95rem;
                line-height:1.6;
            ">
                No data loaded yet.<br>
                Upload a <strong style="color:#F1F5F9;">CSV or Excel</strong> file from the sidebar to begin.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Feature cards ──
    c1, c2, c3 = st.columns(3, gap="medium")

    features = [
        ("📥", "Ingest",
         "Upload raw sales CSV or Excel.<br>Auto schema detection.<br>Zero manual mapping."),
        ("⚙️", "Process",
         "Polars engine handles 200K rows<br>in under 5 seconds.<br>DuckDB SQL analytics."),
        ("📈", "Analyze",
         "4 interactive views:<br>Overview · Regional ·<br>Funnel · Rep Leaderboard."),
    ]

    for col, (icon, title, desc) in zip([c1, c2, c3], features):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="height:100%;text-align:center;">
                    <div style="font-size:2rem;margin-bottom:0.6rem;">{icon}</div>
                    <div style="
                        font-size:1rem;
                        font-weight:700;
                        color:#059669;
                        font-family:Inter,sans-serif;
                        margin-bottom:0.5rem;
                    ">{title}</div>
                    <div style="
                        font-size:0.83rem;
                        color:#94A3B8;
                        font-family:Inter,sans-serif;
                        line-height:1.7;
                    ">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats strip ──
    stats = [
        ("200K", "Max Rows"),
        ("< 5s", "Load Time"),
        ("4", "Analytics Views"),
        ("$0", "Infrastructure"),
        ("10", "Modules"),
    ]

    cols = st.columns(len(stats))
    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align:center;padding:1rem 0.5rem;">
                    <div style="
                        font-size:1.5rem;
                        font-weight:800;
                        color:#FBBF24;
                        font-family:Inter,sans-serif;
                    ">{value}</div>
                    <div style="
                        font-size:0.7rem;
                        text-transform:uppercase;
                        letter-spacing:0.08em;
                        color:#64748B;
                        font-family:Inter,sans-serif;
                        margin-top:4px;
                    ">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════

def render_footer() -> None:
    """Renders the branded footer at the bottom of every page."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="
            border-top:1px solid rgba(5,150,105,0.2);
            padding:1.25rem 0 0.5rem 0;
            margin-top:1rem;
            display:flex;
            justify-content:center;
            align-items:center;
            gap:0.5rem;
            font-family:Inter,sans-serif;
            font-size:0.78rem;
            letter-spacing:0.06em;
            color:#334155;
        ">
            <span style="color:#2D4A42;">//</span>
            <span style="color:#059669;font-weight:700;">ARCHITECTED BY</span>
            <span style="color:#F1F5F9;font-weight:700;">Ali-datasmith</span>
            <span style="color:#2D4A42;">//</span>
            <span>HIGH-PERFORMANCE DATA TERMINAL</span>
            <span style="color:#FBBF24;font-weight:600;">v2.0</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Application entry point.

    Flow:
        1. Build sidebar → get uploaded_file
        2. If file uploaded:
            a. Load → Transform → Seed DuckDB (cached in session_state)
            b. Render SidebarFilters (now data is available)
            c. Render 4 tabbed dashboard views
        3. Else:
            a. Render landing page
        4. Render footer
    """

    uploaded_file = build_sidebar()

    if uploaded_file is not None:

        # ── Data pipeline (re-runs only when file changes) ──
        file_key = uploaded_file.name + str(uploaded_file.size)
        if st.session_state.get("file_key") != file_key:

            with st.spinner("⚡ Processing data..."):
                try:
                    raw_df   = DataIngestor.load_data(uploaded_file)
                    clean_df = DataTransformer.clean_data(raw_df)
                    db_engine.seed_data(clean_df)

                    st.session_state["df"]             = clean_df
                    st.session_state["data_processed"] = True
                    st.session_state["file_key"]       = file_key

                except Exception as e:
                    st.error(f"⚠️ **Ingestion Error:** {e}")
                    st.info(
                        "💡 Ensure your file contains: "
                        "`date`, `revenue`, `rep`, `region`, `product`, `stage`"
                    )
                    st.stop()

        clean_df = st.session_state["df"]

        # ── Sidebar filters (rendered after data is available) ──
        filter_state = SidebarFilters.render(clean_df)

        # ── Dashboard header ──
        section_header(
            "Sales Intelligence Dashboard",
            f"{clean_df.shape[0]:,} records loaded · Filters applied"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── 4 tabbed views ──
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Overview",
            "🗺️ Regional",
            "🌪️ Funnel",
            "👤 Rep Performance"
        ])

        with tab1:
            DashboardViews.show_overview(clean_df, filter_state)
        with tab2:
            DashboardViews.show_regional_breakdown(clean_df, filter_state)
        with tab3:
            DashboardViews.show_funnel_analysis(clean_df, filter_state)
        with tab4:
            DashboardViews.show_rep_performance(clean_df, filter_state)

    else:
        render_landing()

    render_footer()


# ── Entry point ──
if __name__ == "__main__":
    main()
