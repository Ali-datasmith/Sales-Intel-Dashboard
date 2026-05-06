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

# ============================================================
#  MASTER THEME — ULTRA PROFESSIONAL DARK TERMINAL
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@600;700;800&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --cyan:        #00E5FF;
    --cyan-dim:    #00B8CC;
    --cyan-glow:   rgba(0, 229, 255, 0.15);
    --green:       #00FF88;
    --green-glow:  rgba(0, 255, 136, 0.15);
    --amber:       #FFB300;
    --red:         #FF4757;
    --bg:          #080810;
    --bg2:         #0C0C18;
    --bg3:         #111122;
    --surface:     rgba(255,255,255,0.03);
    --border:      rgba(0, 229, 255, 0.12);
    --border-hot:  rgba(0, 229, 255, 0.40);
    --text:        #E2E8F0;
    --text-dim:    #64748B;
    --text-muted:  #334155;
    --font-mono:   'JetBrains Mono', 'Space Mono', monospace;
    --font-display:'Syne', sans-serif;
}

/* ── GLOBAL RESET ── */
* { box-sizing: border-box; }

html, body, [data-testid="stApp"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
}

/* ── SCANLINE OVERLAY ── */
[data-testid="stApp"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,229,255,0.012) 2px,
        rgba(0,229,255,0.012) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── GRID BACKGROUND ── */
[data-testid="stApp"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,229,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,229,255,0.025) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

/* ── MAIN CONTENT AREA ── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ── HEADINGS ── */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-display) !important;
    color: var(--cyan) !important;
    letter-spacing: -0.5px;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border-hot) !important;
    box-shadow: 4px 0 40px rgba(0,229,255,0.06) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* ── SIDEBAR LABELS ── */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown p {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 1px solid var(--border-hot) !important;
    border-radius: 6px !important;
    box-shadow: 0 0 20px var(--cyan-glow), inset 0 0 20px rgba(0,229,255,0.02) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploader"]:hover {
    box-shadow: 0 0 35px rgba(0,229,255,0.25), inset 0 0 30px rgba(0,229,255,0.04) !important;
    border-color: var(--cyan) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}

/* ── BUTTONS — PRIMARY ── */
div.stButton > button {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border-hot) !important;
    border-radius: 4px !important;
    padding: 10px 20px !important;
    transition: all 0.25s ease !important;
    clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 8px 100%, 0 calc(100% - 8px));
}

div.stButton > button:hover {
    background: var(--cyan-glow) !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 20px var(--cyan-glow) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
}

/* ── DOWNLOAD BUTTON ── */
div.stDownloadButton > button {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: var(--green) !important;
    border: 1px solid rgba(0,255,136,0.4) !important;
    border-radius: 4px !important;
    padding: 10px 20px !important;
    transition: all 0.25s ease !important;
    clip-path: polygon(0 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 8px 100%, 0 calc(100% - 8px));
}

div.stDownloadButton > button:hover {
    background: var(--green-glow) !important;
    border-color: var(--green) !important;
    box-shadow: 0 0 20px var(--green-glow) !important;
    color: #fff !important;
    transform: translateY(-1px) !important;
}

/* ── TABS ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}

[data-baseweb="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
    background: transparent !important;
    border: none !important;
    padding: 12px 24px !important;
    transition: all 0.2s !important;
}

[data-baseweb="tab"]:hover {
    color: var(--cyan) !important;
    background: var(--cyan-glow) !important;
}

[data-baseweb="tab"][aria-selected="true"] {
    color: var(--cyan) !important;
    background: var(--cyan-glow) !important;
}

div[data-baseweb="tab-highlight"] {
    background: var(--cyan) !important;
    height: 2px !important;
}

/* ── MULTISELECT TAGS ── */
span[data-baseweb="tag"] {
    background: rgba(0,229,255,0.08) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border-hot) !important;
    border-radius: 3px !important;
    font-family: var(--font-mono) !important;
    font-size: 11px !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 20px !important;
    transition: all 0.3s !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-hot) !important;
    box-shadow: 0 0 20px var(--cyan-glow) !important;
}

[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-dim) !important;
}

[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: var(--cyan) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}

/* ── SELECTBOX & SLIDERS ── */
[data-baseweb="select"] {
    background: var(--bg3) !important;
    border-color: var(--border) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: var(--cyan) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border-hot); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* ── PLOTLY CHARTS ── */
.js-plotly-plot { border-radius: 6px !important; }

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── INFO / WARNING BOXES ── */
[data-testid="stAlert"] {
    background: var(--surface) !important;
    border-radius: 4px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
}

/* ── PULSE ANIMATION ── */
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(0,229,255,0.4); }
    70%  { box-shadow: 0 0 0 8px rgba(0,229,255,0); }
    100% { box-shadow: 0 0 0 0 rgba(0,229,255,0); }
}

@keyframes typing {
    from { width: 0 }
    to   { width: 100% }
}

@keyframes blink-caret {
    from, to { border-color: transparent }
    50%      { border-color: var(--cyan); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes glow-pulse {
    0%, 100% { opacity: 0.6; }
    50%       { opacity: 1; }
}

/* ── STATUS BADGE ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-family: var(--font-mono);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border: 1px solid var(--cyan);
    color: var(--cyan);
    animation: pulse-ring 2.5s infinite;
    margin-bottom: 16px;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--cyan);
    animation: glow-pulse 1.5s infinite;
}

/* ── TERMINAL BOX ── */
.terminal-box {
    background: rgba(0,229,255,0.03);
    border: 1px solid var(--border-hot);
    border-radius: 6px;
    padding: 28px 32px;
    text-align: center;
    font-family: var(--font-mono);
    font-size: 14px;
    color: var(--text-dim);
    letter-spacing: 1px;
    box-shadow: 0 0 30px var(--cyan-glow), inset 0 0 30px rgba(0,229,255,0.02);
    animation: fadeInUp 0.6s ease forwards;
}

/* ── HERO SECTION ── */
.hero-container {
    padding: 20px 0 40px 0;
    animation: fadeInUp 0.5s ease forwards;
}

.hero-eyebrow {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 32px;
    height: 1px;
    background: var(--cyan);
}

.hero-title {
    font-family: var(--font-display);
    font-size: clamp(42px, 6vw, 76px);
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 0.95;
    color: var(--text) !important;
    margin-bottom: 4px;
}

.hero-title .accent {
    color: var(--cyan) !important;
    -webkit-text-stroke: 0px;
}

.hero-subtitle {
    font-family: var(--font-mono);
    font-size: 13px;
    color: var(--text-dim);
    letter-spacing: 1px;
    margin: 20px 0 0 0;
    line-height: 1.8;
}

/* ── FEATURE CARDS ── */
.feat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 24px;
    transition: all 0.3s ease;
    animation: fadeInUp 0.6s ease forwards;
    height: 100%;
}

.feat-card:hover {
    border-color: var(--border-hot);
    box-shadow: 0 0 24px var(--cyan-glow);
    transform: translateY(-3px);
}

.feat-icon { font-size: 28px; margin-bottom: 12px; }

.feat-title {
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 700;
    color: var(--cyan) !important;
    margin-bottom: 8px;
}

.feat-desc {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-dim);
    line-height: 1.8;
    letter-spacing: 0.5px;
}

/* ── TYPEWRITER ── */
.typewriter-wrap {
    overflow: hidden;
    display: inline-block;
}

.typewriter-text {
    font-family: var(--font-display);
    font-size: clamp(22px, 3vw, 36px);
    font-weight: 700;
    color: var(--cyan) !important;
    overflow: hidden;
    border-right: 2px solid var(--cyan);
    white-space: nowrap;
    animation: typing 2.5s steps(30, end), blink-caret 0.75s step-end infinite;
}

/* ── KPI STRIP ── */
.kpi-strip {
    display: flex;
    gap: 2px;
    margin: 24px 0;
}

.kpi-item {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 16px 20px;
    text-align: center;
    transition: all 0.3s;
}

.kpi-item:hover {
    border-color: var(--border-hot);
    background: var(--cyan-glow);
}

.kpi-value {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 800;
    color: var(--cyan);
}

.kpi-label {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-top: 4px;
}

/* ── FOOTER ── */
.footer-strip {
    border-top: 1px solid var(--border);
    padding: 20px 0 8px 0;
    margin-top: 40px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 1.5px;
    color: var(--text-muted);
}

.footer-accent { color: var(--cyan); font-weight: 700; }
.footer-name   { color: var(--text); font-weight: 700; }

/* ── SIDEBAR SECTION HEADER ── */
.sidebar-section {
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--cyan);
    padding: 12px 0 8px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
}

/* ── TOOLTIP / INFO BADGE ── */
.info-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    background: rgba(255,179,0,0.08);
    border: 1px solid rgba(255,179,0,0.25);
    border-radius: 3px;
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--amber);
    letter-spacing: 0.5px;
}

/* ── HIDE STREAMLIT BRANDING ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================
#  SIDEBAR BUILDER
# ============================================================
def build_sidebar():
    with st.sidebar:

        # ── Status Badge ──
        is_active = "df" in st.session_state and st.session_state.df is not None
        status_label = "POLARS ACTIVE" if is_active else "SYSTEM IDLE"
        status_color = "#00E5FF" if is_active else "#64748B"
        st.markdown(f"""
        <div class="status-badge" style="border-color:{status_color}; color:{status_color};">
            <div class="status-dot" style="background:{status_color};"></div>
            {status_label}
        </div>
        """, unsafe_allow_html=True)

        # ── Data Ingestion ──
        st.markdown('<div class="sidebar-section">📥 &nbsp;Data Ingestion</div>', unsafe_allow_html=True)
        st.caption("Upload CRM Export")
        uploaded_file = st.file_uploader(
            label="upload",
            type=["csv", "xlsx"],
            label_visibility="collapsed"
        )
        st.caption("200MB per file • CSV, XLSX")

        sample_csv = generate_sample_data()
        st.download_button(
            label="⬇ Get Sample CRM Data",
            data=sample_csv,
            file_name="sample_crm_data.csv",
            mime="text/csv",
            use_container_width=True
        )

        return uploaded_file


# ============================================================
#  LANDING PAGE
# ============================================================
def render_landing():
    # ── Hero ──
    st.markdown("""
    <div class="hero-container">
        <div class="hero-eyebrow">High-Performance Data Terminal</div>
        <div class="hero-title">
            ⚡ Sales Intel<br>
            <span class="accent">Terminal</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Typewriter ──
    st.markdown("""
    <div class="typewriter-wrap">
        <div class="typewriter-text">Ready to Generate Insights</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Terminal Waiting Box ──
    st.markdown("""
    <div class="terminal-box">
        <span style="color:#334155;">❯ &nbsp;</span>
        Terminal awaiting CRM data stream via Sidebar.
        <span style="display:inline-block;width:8px;height:14px;background:#00E5FF;
               vertical-align:middle;margin-left:4px;animation:blink-caret 1s step-end infinite;">
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Feature Cards ──
    c1, c2, c3 = st.columns(3, gap="small")

    with c1:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon">📥</div>
            <div class="feat-title">Ingest</div>
            <div class="feat-desc">
                Upload raw sales CSV / Excel.<br>
                Auto schema detection.<br>
                Zero manual mapping.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon">⚙️</div>
            <div class="feat-title">Process</div>
            <div class="feat-desc">
                Polars engine optimises<br>
                200K rows in &lt; 5 seconds.<br>
                DuckDB SQL analytics.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feat-card">
            <div class="feat-icon">📈</div>
            <div class="feat-title">Analyze</div>
            <div class="feat-desc">
                4 interactive views:<br>
                Overview · Regional ·<br>
                Funnel · Rep Leaderboard.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI Strip ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="kpi-strip">
        <div class="kpi-item">
            <div class="kpi-value">200K</div>
            <div class="kpi-label">Max Rows</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-value">&lt; 5s</div>
            <div class="kpi-label">Load Time</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-value">4</div>
            <div class="kpi-label">Analytics Views</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-value">$0</div>
            <div class="kpi-label">Infrastructure</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-value">10</div>
            <div class="kpi-label">Modules</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#  FOOTER
# ============================================================
def render_footer():
    st.markdown("""
    <div class="footer-strip">
        <span style="color:#334155;">//</span>
        <span class="footer-accent">ARCHITECTED BY</span>
        <span class="footer-name">Ali-datasmith</span>
        <span style="color:#334155;">//</span>
        <span>HIGH-PERFORMANCE DATA TERMINAL</span>
        <span class="footer-accent">v1.0</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#  MAIN
# ============================================================
def main():
    uploaded_file = build_sidebar()

    if uploaded_file is not None:
        # ── Load & process data ──
        with st.spinner("⚡ Polars engine initialising..."):
            try:
                ingestor    = DataIngestor()
                raw_df      = ingestor.load(uploaded_file)
                transformer = DataTransformer()
                clean_df    = transformer.clean(raw_df)
                engine      = db_engine()
                engine.register("sales", clean_df)
                st.session_state.df     = clean_df
                st.session_state.engine = engine
            except Exception as e:
                st.error(f"⚠ Ingestion error: {e}")
                st.info(
                    "💡 Ensure your CSV contains all required columns: "
                    "`date`, `revenue`, `rep`, `region`, `product`, `stage`"
                )
                st.stop()

        # ── Build sidebar filters now data is loaded ──
        filters = SidebarFilters(st.session_state.df)
        filter_state = filters.render()

        # ── Render dashboard views ──
        views = DashboardViews(
            df=st.session_state.df,
            engine=st.session_state.engine,
            filters=filter_state
        )
        views.render()

    else:
        render_landing()

    render_footer()


if __name__ == "__main__":
    main()
