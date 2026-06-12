"""
app.py - Entry Point for Sales Intel Terminal v2.0

Responsibilities:
    1. Page config (called ONCE)
    2. CSS / theme injection
    3. Login gate
    4. Premium sidebar — user panel + status + uploader
    5. Data pipeline — ingest → transform → seed DuckDB (file-key cached)
    6. Branded header bar (render_header)
    7. Dashboard routing — 4 tabbed views
    8. Landing page — hero + feature cards + stats strip
    9. Footer
"""

import streamlit as st
from typing import Optional

from theme import (
    inject_css, section_header, status_badge, pulse_dot, render_header,
    PRIMARY_EMERALD, ACCENT_GOLD, SECONDARY_TEAL, SUCCESS_GREEN,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    GLASS_BG, GLASS_BORDER, GLASS_SHADOW,
    SURFACE_1, SURFACE_2, BG_DARK
)
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
    page_title="Sales Intel Terminal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# ══════════════════════════════════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════════════════════════════════

if not st.session_state.get("authenticated", False):
    render_login()
    st.stop()


# ══════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════

def build_sidebar() -> Optional[st.runtime.uploaded_file_manager.UploadedFile]:
    """
    Renders the premium sidebar layout including system telemetry,
    user identities, and custom data dropzones.

    Returns:
        Optional[UploadedFile]: The raw file handle uploaded by the client.
    """
    with st.sidebar:
        # ── Logo strip ──
        st.markdown(
            f"""
            <div style="
                padding:1.2rem 0 1rem 0;
                border-bottom:1px solid {GLASS_BORDER};
                margin-bottom:1.25rem;
                animation:fadeInUp 0.3s ease;
            ">
                <div style="
                    font-family:Space Grotesk,sans-serif;
                    font-size:1.05rem;
                    font-weight:800;
                    color:{TEXT_PRIMARY};
                    letter-spacing:-0.02em;
                    margin-bottom:2px;
                ">📊 SALES INTEL <span style="color:{PRIMARY_EMERALD};">TERMINAL</span></div>
                <div style="
                    font-family:JetBrains Mono,monospace;
                    font-size:0.62rem;
                    color:{TEXT_MUTED};
                    letter-spacing:0.12em;
                    text-transform:uppercase;
                ">v2.0 · High-Performance Analytics</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── User identity panel ──
        username = st.session_state.get("username", "user")
        display_name = st.session_state.get("display_name", username.title())
        role = st.session_state.get("role", "viewer")
        role_color = ACCENT_GOLD if role == "admin" else SECONDARY_TEAL

        st.markdown(
            f"""
            <div style="
                background:{GLASS_BG};
                border:1px solid {GLASS_BORDER};
                border-radius:12px;
                padding:0.9rem 1rem;
                margin-bottom:1rem;
                animation:fadeInUp 0.35s ease;
            ">
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;                ">
                    <div>
                        <div style="
                            font-family:Space Grotesk,sans-serif;
                            font-size:0.88rem;
                            font-weight:700;
                            color:{TEXT_PRIMARY};
                            margin-bottom:3px;
                        ">👤 {display_name}</div>
                        <div style="
                            font-family:JetBrains Mono,monospace;
                            font-size:0.62rem;
                            color:{role_color};
                            text-transform:uppercase;
                            letter-spacing:0.1em;
                        ">{role}</div>
                    </div>
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.62rem;
                        color:{SUCCESS_GREEN};
                        letter-spacing:0.08em;
                    ">{pulse_dot('success')} AUTH</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        render_logout_button()
        st.markdown("<br>", unsafe_allow_html=True)

        # ── System status ──
        is_active = st.session_state.get("data_processed", False)
        records = st.session_state.get("df").shape[0] if is_active and "df" in st.session_state else 0

        if is_active:
            st.markdown(
                f"""
                <div style="
                    background:rgba(16,185,129,0.08);
                    border:1px solid rgba(16,185,129,0.25);
                    border-radius:10px;
                    padding:0.7rem 1rem;
                    margin-bottom:1rem;
                    animation:fadeInUp 0.4s ease;
                ">
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.68rem;
                        color:{SUCCESS_GREEN};
                        text-transform:uppercase;
                        letter-spacing:0.1em;
                        font-weight:600;
                        margin-bottom:4px;
                    ">{pulse_dot('success')} DATA LOADED</div>
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.65rem;
                        color:{TEXT_SECONDARY};
                        letter-spacing:0.05em;
                    ">{records:,} records in memory</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="
                    background:{GLASS_BG};
                    border:1px solid {GLASS_BORDER};
                    border-radius:10px;
                    padding:0.7rem 1rem;
                    margin-bottom:1rem;
                ">
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.68rem;
                        color:{TEXT_MUTED};
                        text-transform:uppercase;
                        letter-spacing:0.1em;
                    ">○ AWAITING DATA</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ── Divider ──
        st.markdown(
            f"""
            <div style="
                font-family:JetBrains Mono,monospace;
                font-size:0.65rem;
                text-transform:uppercase;
                letter-spacing:0.14em;
                color:{PRIMARY_EMERALD};
                font-weight:600;
                padding-bottom:0.6rem;
                border-bottom:1px solid {GLASS_BORDER};
                margin-bottom:0.8rem;
            ">📥 Data Ingestion</div>
            """,
            unsafe_allow_html=True
        )

        st.caption("Upload your CRM export — CSV or Excel")
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

        # ── Tech stack strip ──
        st.markdown(
            f"""
            <div style="
                margin-top:2rem;                padding-top:1rem;                border-top:1px solid {GLASS_BORDER};            ">
                <div style="
                    font-family:JetBrains Mono,monospace;                    font-size:0.6rem;                    text-transform:uppercase;                    letter-spacing:0.1em;                    color:{TEXT_MUTED};                    margin-bottom:0.5rem;                ">Powered By</div>
                <div style="
                    font-family:JetBrains Mono,monospace;                    font-size:0.62rem;                    color:{TEXT_SECONDARY};                    line-height:1.9;                    letter-spacing:0.04em;                ">
                    <span style="color:{PRIMARY_EMERALD};">▸</span> Polars 1.0 · Rust Engine<br>
                    <span style="color:{PRIMARY_EMERALD};">▸</span> DuckDB 1.0 · In-Memory SQL<br>
                    <span style="color:{PRIMARY_EMERALD};">▸</span> Plotly 5.22 · Interactive Charts<br>
                    <span style="color:{PRIMARY_EMERALD};">▸</span> Streamlit 1.36 · UI Layer                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    return uploaded_file


# ══════════════════════════════════════════════════════════════════
# LANDING PAGE
# ══════════════════════════════════════════════════════════════════

def render_landing() -> None:
    """Premium hero landing page shown when no data is loaded."""
    # ── Hero section ──
    st.markdown(
        f"""
        <div style="padding:2.5rem 0 1rem 0;animation:fadeInUp 0.5s ease;">
            <div style="
                font-family:JetBrains Mono,monospace;
                font-size:0.72rem;
                letter-spacing:0.2em;
                text-transform:uppercase;
                color:{PRIMARY_EMERALD};
                font-weight:600;
                margin-bottom:1rem;
            ">{pulse_dot('success')} &nbsp;HIGH-PERFORMANCE SALES ANALYTICS TERMINAL</div>
            <h1 style="
                font-family:Space Grotesk,sans-serif;
                font-size:clamp(2.8rem,5vw,4.5rem);
                font-weight:800;
                letter-spacing:-0.04em;
                line-height:1.0;
                color:{TEXT_PRIMARY};
                margin:0 0 0.6rem 0;
            ">
                SALES INTEL<br>
                <span style="
                    color:{PRIMARY_EMERALD};
                    text-shadow:0 0 40px rgba(5,150,105,0.4);
                ">TERMINAL</span>
            </h1>
            <p style="
                font-family:Space Grotesk,sans-serif;
                font-size:1.05rem;
                color:{TEXT_SECONDARY};
                margin:1rem 0 0 0;
                max-width:560px;
                line-height:1.65;
                font-weight:400;
            ">
                Upload your CRM export from the sidebar to generate
                instant revenue insights, pipeline analysis,
                and rep performance dashboards — zero configuration.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Upload CTA card ──
    st.markdown(
        f"""
        <div class="glass-card" style="
            text-align:center;
            padding:2.5rem 2rem;
            margin:1.5rem 0 2rem 0;
            border:1px dashed rgba(5,150,105,0.35);
        ">
            <div style="font-size:3rem;margin-bottom:1rem;">📂</div>
            <div style="                font-family:Space Grotesk,sans-serif;                font-weight:700;                font-size:1.1rem;                color:{TEXT_PRIMARY};                margin-bottom:0.5rem;            ">No Data Loaded</div>
            <div style="                font-family:JetBrains Mono,monospace;                color:{TEXT_SECONDARY};                font-size:0.78rem;                letter-spacing:0.05em;                line-height:1.8;            ">
                Upload a <span style="color:{ACCENT_GOLD};font-weight:600;">CSV</span>
                or <span style="color:{ACCENT_GOLD};font-weight:600;">Excel</span>
                file from the sidebar to begin.<br>
                Or download the sample dataset to explore the dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ── Feature cards ──
    features = [
        ("📥", "Ingest", "Upload raw sales CSV or Excel. Auto schema detection. Zero manual column mapping required."),
        ("⚙️", "Process", "Polars Rust engine handles 200K rows in under 5 seconds. DuckDB powers all SQL analytics."),
        ("🌪️", "Funnel", "Stage-by-stage drop-off analysis. Conversion rates from Prospecting → Closed Won."),
        ("📈", "Analyze", "4 interactive views: Overview, Regional Heatmap, Funnel, Rep Leaderboard Scorecard."),
    ]

    cols = st.columns(4, gap="medium")
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="height:100%;text-align:center;padding:1.5rem 1rem;">
                    <div style="font-size:2rem;margin-bottom:0.75rem;">{icon}</div>
                    <div style="
                        font-family:Space Grotesk,sans-serif;
                        font-size:0.88rem;
                        font-weight:700;
                        color:{PRIMARY_EMERALD};
                        text-transform:uppercase;
                        letter-spacing:0.05em;
                        margin-bottom:0.6rem;
                    ">{title}</div>
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.72rem;
                        color:{TEXT_SECONDARY};
                        line-height:1.75;
                        letter-spacing:0.02em;
                    ">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Stats strip ──
    stats = [
        ("200K", "MAX ROWS"),
        ("< 5s", "LOAD TIME"),
        ("4", "VIEWS"),
        ("1.0", "POLARS"),
        ("1.0", "DUCKDB"),
        ("$0", "INFRA COST"),
    ]

    cols = st.columns(len(stats))
    for col, (value, label) in zip(cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="text-align:center;padding:1.1rem 0.5rem;">
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:1.5rem;
                        font-weight:700;
                        color:{ACCENT_GOLD};
                        text-shadow:0 0 16px rgba(251,191,36,0.25);
                        line-height:1;
                        margin-bottom:6px;
                    ">{value}</div>
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.6rem;
                        text-transform:uppercase;
                        letter-spacing:0.12em;
                        color:{TEXT_MUTED};
                    ">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Schema guide ──
    section_header(
        "Expected Data Schema",
        "ENSURE YOUR CSV OR EXCEL CONTAINS THESE COLUMNS"
    )

    schema_cols = st.columns(3, gap="medium")
    schema = [
        ("date", "Date of the deal/transaction", "2024-01-15"),
        ("revenue", "Deal value (numeric or $string)", "$1,200.00"),
        ("rep", "Sales representative name", "Alice Johnson"),
        ("region", "Geographic region or territory", "North America"),
        ("product", "Product or service sold", "Enterprise Plan"),
        ("stage", "CRM pipeline stage", "Closed Won"),
    ]

    for i, (col_name, desc, example) in enumerate(schema):
        with schema_cols[i % 3]:
            st.markdown(
                f"""
                <div style="
                    background:{GLASS_BG};
                    border:1px solid {GLASS_BORDER};
                    border-radius:10px;
                    padding:0.85rem 1rem;
                    margin-bottom:0.6rem;
                    animation:fadeInUp {0.3 + i*0.05:.2f}s ease;
                ">
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.8rem;
                        font-weight:600;
                        color:{PRIMARY_EMERALD};
                        margin-bottom:3px;
                    ">{col_name}</div>
                    <div style="
                        font-family:Space Grotesk,sans-serif;
                        font-size:0.75rem;
                        color:{TEXT_SECONDARY};
                        margin-bottom:4px;
                    ">{desc}</div>
                    <div style="
                        font-family:JetBrains Mono,monospace;
                        font-size:0.68rem;
                        color:{TEXT_MUTED};
                        letter-spacing:0.04em;
                    ">e.g. {example}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ══════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════

def render_footer() -> None:
    """Renders data terminal bottom credits and engine statuses."""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            border-top:1px solid {GLASS_BORDER};
            padding:1.25rem 0 0.75rem 0;
            margin-top:1rem;
            display:flex;
            justify-content:space-between;
            align-items:center;
            animation:fadeIn 0.5s ease;
        ">
            <div style="
                font-family:JetBrains Mono,monospace;
                font-size:0.7rem;
                letter-spacing:0.08em;
                color:{TEXT_MUTED};
            ">
                <span style="color:{PRIMARY_EMERALD};font-weight:700;">// SALES INTEL TERMINAL</span>
                &nbsp;·&nbsp; v2.0
                &nbsp;·&nbsp; ARCHITECTED BY
                <span style="color:{TEXT_PRIMARY};font-weight:700;">ALI-DATASMITH</span>
            </div>
            <div style="
                font-family:JetBrains Mono,monospace;
                font-size:0.65rem;
                color:{TEXT_MUTED};
                letter-spacing:0.08em;
            ">
                POLARS · DUCKDB · PLOTLY · STREAMLIT
                &nbsp;·&nbsp;
                <span style="color:{ACCENT_GOLD};">HIGH-PERFORMANCE DATA TERMINAL</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════
# MAIN ROUTER LOOP
# ══════════════════════════════════════════════════════════════════

def main() -> None:
    """
    Application core runner. Handles unified processing state pipelines
    and lazy-renders active tab dashboard modules.
    """
    uploaded_file = build_sidebar()

    if uploaded_file is not None:
        # ── Data pipeline — cached by file identity ──
        file_key = uploaded_file.name + str(uploaded_file.size)

        if st.session_state.get("file_key") != file_key:
            with st.spinner("⚡ Processing your data..."):
                try:
                    raw_df = DataIngestor.load_data(uploaded_file)
                    clean_df = DataTransformer.clean_data(raw_df)
                    db_engine.seed_data(clean_df)

                    st.session_state["df"] = clean_df
                    st.session_state["data_processed"] = True
                    st.session_state["file_key"] = file_key

                    st.success(
                        f"✅ Loaded **{clean_df.shape[0]:,} records** "
                        f"across **{clean_df.shape[1]} columns** — ready."
                    )
                except Exception as e:
                    st.markdown(
                        f"""
                        <div style="
                            background:rgba(239,68,68,0.08);
                            border:1px solid rgba(239,68,68,0.3);
                            border-radius:12px;
                            padding:1.25rem 1.5rem;
                            font-family:JetBrains Mono,monospace;
                            font-size:0.82rem;
                        ">
                            <div style="color:#EF4444;font-weight:700;margin-bottom:0.5rem;">
                                ⚠ INGESTION ERROR
                            </div>                            <div style="color:{TEXT_SECONDARY};">{e}</div>                            <div style="color:{TEXT_MUTED};margin-top:0.5rem;font-size:0.72rem;">                                Ensure columns: date · revenue · rep · region · product · stage                            </div>                        </div>                        """,
                        unsafe_allow_html=True
                    )
                    st.stop()

        clean_df = st.session_state["df"]

        # ── Sidebar filters ──
        filter_state = SidebarFilters.render(clean_df)

        # ── Branded header bar ──
        username = st.session_state.get("display_name", "User")
        render_header(records=clean_df.shape[0], username=username)

        # ── 4 tabbed views ──
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊  Overview",
            "🗺️  Regional",
            "🌪️  Funnel",
            "👤  Rep Performance",
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


if __name__ == "__main__":
    main()
