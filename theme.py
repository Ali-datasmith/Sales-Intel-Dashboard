"""
theme.py - Visual Identity for Sales Intel Terminal.

Defines:
- Emerald + Gold branded color palette
- Plotly 'sales_intel_dark' custom template
- Glass-morphism CSS injected via st.markdown()
- Helper utilities for consistent UI elements
"""

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ══════════════════════════════════════════════════════════════════
# COLOR PALETTE — Emerald + Gold
# ══════════════════════════════════════════════════════════════════

# Primary
PRIMARY_EMERALD   = "#059669"   # Deep Emerald — primary brand, main KPIs
ACCENT_GOLD       = "#FBBF24"   # Gold — success, closed deals, premium highlights
SECONDARY_TEAL    = "#0D9488"   # Teal — secondary charts, supporting data

# Status Colors
SUCCESS_GREEN     = "#10B981"   # Positive trends, growth indicators
WARNING_AMBER     = "#F59E0B"   # At-risk, slow stages
DANGER_RED        = "#DC2626"   # Negative deltas, drop-offs, alerts
INFO_BLUE         = "#3B82F6"   # Neutral information, tooltips

# Surface / Background
BG_DARK           = "#0A0F0D"   # Main page background (very dark green-black)
SURFACE_1         = "#111814"   # Primary card surface (dark, slight green tint)
SURFACE_2         = "#1A2420"   # Secondary card / sidebar surface
SURFACE_3         = "#243330"   # Hover states, active panels
BORDER_COLOR      = "#2D4A42"   # Subtle border (muted teal)
BORDER_GLOW       = "#059669"   # Hover border glow (Emerald)

# Text
TEXT_PRIMARY      = "#F1F5F9"   # Main text (near-white)
TEXT_SECONDARY    = "#94A3B8"   # Dimmed labels, captions
TEXT_MUTED        = "#64748B"   # Placeholders, disabled states

# Glass-morphism Layer
GLASS_BG          = "rgba(5, 150, 105, 0.06)"    # Transparent emerald wash
GLASS_BORDER      = "rgba(5, 150, 105, 0.25)"    # Frosted Emerald border
GLASS_BLUR        = "blur(12px)"                  # Backdrop blur amount
GLASS_SHADOW      = "0 8px 32px rgba(5, 150, 105, 0.12)"  # Card shadow

# Color sequence for multi-series charts
CHART_COLOR_SEQUENCE = [
    PRIMARY_EMERALD,    # Series 1
    ACCENT_GOLD,        # Series 2
    SECONDARY_TEAL,     # Series 3
    SUCCESS_GREEN,      # Series 4
    WARNING_AMBER,      # Series 5
    INFO_BLUE,          # Series 6
    DANGER_RED          # Series 7
]


# ══════════════════════════════════════════════════════════════════
# PLOTLY TEMPLATE — sales_intel_dark
# ══════════════════════════════════════════════════════════════════

def apply_custom_theme() -> None:
    """
    Builds and registers the 'sales_intel_dark' Plotly template globally.
    Call once at app startup in app.py before any chart rendering.
    """
    template = go.layout.Template()

    template.layout = go.Layout(
        # ── Canvas ──
        plot_bgcolor  = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)",

        # ── Typography ──
        font=dict(
            family = "Inter, system-ui, sans-serif",
            color  = TEXT_PRIMARY,
            size   = 12
        ),

        # ── Title ──
        title=dict(
            font=dict(
                family = "Inter, system-ui, sans-serif",
                size   = 18,
                color  = TEXT_PRIMARY
            ),
            x        = 0.5,
            xanchor  = "center"
        ),

        # ── Axes ──
        xaxis=dict(
            gridcolor       = SURFACE_3,
            zerolinecolor   = SURFACE_3,
            linecolor       = BORDER_COLOR,
            tickfont        = dict(color=TEXT_SECONDARY, size=11),
            showgrid        = True,
            showline        = True,
            zeroline        = False
        ),
        yaxis=dict(
            gridcolor       = SURFACE_3,
            zerolinecolor   = SURFACE_3,
            linecolor       = BORDER_COLOR,
            tickfont        = dict(color=TEXT_SECONDARY, size=11),
            showgrid        = True,
            showline        = True,
            zeroline        = False
        ),

        # ── Legend ──
        legend=dict(
            orientation  = "h",
            yanchor      = "bottom",
            y            = 1.02,
            xanchor      = "right",
            x            = 1,
            font         = dict(color=TEXT_SECONDARY, size=11),
            bgcolor      = "rgba(0,0,0,0)",
            bordercolor  = BORDER_COLOR,
            borderwidth  = 1
        ),

        # ── Hover ──
        hoverlabel=dict(
            bgcolor     = SURFACE_2,
            bordercolor = PRIMARY_EMERALD,
            font        = dict(
                family = "Inter, system-ui, sans-serif",
                size   = 12,
                color  = TEXT_PRIMARY
            )
        ),

        # ── Margins ──
        margin = dict(t=60, b=50, l=50, r=30),

        # ── Color Sequence ──
        colorway = CHART_COLOR_SEQUENCE
    )

    pio.templates["sales_intel_dark"] = template
    pio.templates.default = "sales_intel_dark"


# ══════════════════════════════════════════════════════════════════
# GLASS-MORPHISM CSS — injected via st.markdown()
# ══════════════════════════════════════════════════════════════════

GLASSMORPHISM_CSS = f"""
<style>
/* ── Google Font Import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {{
    font-family: 'Inter', system-ui, sans-serif !important;
}}

/* ── Page Background ── */
.stApp {{
    background: linear-gradient(
        135deg,
        {BG_DARK} 0%,
        #0D1A14 50%,
        {BG_DARK} 100%
    ) !important;
    background-attachment: fixed !important;
}}

/* ── Glass Card (base class) ── */
.glass-card {{
    background: {GLASS_BG} !important;
    backdrop-filter: {GLASS_BLUR} !important;
    -webkit-backdrop-filter: {GLASS_BLUR} !important;
    border: 1px solid {GLASS_BORDER} !important;
    border-radius: 16px !important;
    box-shadow: {GLASS_SHADOW} !important;
    padding: 1.5rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}

.glass-card:hover {{
    border-color: {BORDER_GLOW} !important;
    box-shadow: 0 12px 40px rgba(5, 150, 105, 0.22) !important;
}}

/* ── KPI Metric Cards ── */
[data-testid="metric-container"] {{
    background: {GLASS_BG} !important;
    backdrop-filter: {GLASS_BLUR} !important;
    -webkit-backdrop-filter: {GLASS_BLUR} !important;
    border: 1px solid {GLASS_BORDER} !important;
    border-radius: 14px !important;
    box-shadow: {GLASS_SHADOW} !important;
    padding: 1rem 1.25rem !important;
    transition: all 0.2s ease !important;
}}

[data-testid="metric-container"]:hover {{
    border-color: {PRIMARY_EMERALD} !important;
    box-shadow: 0 0 20px rgba(5, 150, 105, 0.3) !important;
    transform: translateY(-2px) !important;
}}

[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {ACCENT_GOLD} !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}}

[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    color: {TEXT_SECONDARY} !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}}

[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        {SURFACE_1} 0%,
        {SURFACE_2} 100%
    ) !important;
    border-right: 1px solid {GLASS_BORDER} !important;
    backdrop-filter: {GLASS_BLUR} !important;
}}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label {{
    color: {TEXT_SECONDARY} !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    font-weight: 500 !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {SURFACE_1} !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid {GLASS_BORDER} !important;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 9px !important;
    color: {TEXT_SECONDARY} !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    padding: 0.5rem 1.25rem !important;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(
        135deg,
        {PRIMARY_EMERALD},
        {SECONDARY_TEAL}
    ) !important;
    color: {TEXT_PRIMARY} !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 12px rgba(5, 150, 105, 0.35) !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(
        135deg,
        {PRIMARY_EMERALD},
        {SECONDARY_TEAL}
    ) !important;
    color: {TEXT_PRIMARY} !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.03em !important;
}}

.stButton > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(5, 150, 105, 0.45) !important;
}}

.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* ── Input Fields ── */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stMultiSelect > div > div {{
    background: {SURFACE_2} !important;
    border: 1px solid {BORDER_COLOR} !important;
    border-radius: 10px !important;
    color: {TEXT_PRIMARY} !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease !important;
}}

.stTextInput > div > div > input:focus {{
    border-color: {PRIMARY_EMERALD} !important;
    box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.2) !important;
    outline: none !important;
}}

/* ── DataFrames / Tables ── */
[data-testid="stDataFrame"] {{
    background: {GLASS_BG} !important;
    border: 1px solid {GLASS_BORDER} !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}}

/* ── Plotly Charts Container ── */
[data-testid="stPlotlyChart"] {{
    background: {GLASS_BG} !important;
    backdrop-filter: {GLASS_BLUR} !important;
    border: 1px solid {GLASS_BORDER} !important;
    border-radius: 16px !important;
    padding: 0.5rem !important;
    box-shadow: {GLASS_SHADOW} !important;
}}

/* ── Alert / Info Boxes ── */
.stAlert {{
    background: {GLASS_BG} !important;
    border: 1px solid {GLASS_BORDER} !important;
    border-radius: 12px !important;
    backdrop-filter: {GLASS_BLUR} !important;
}}

/* ── Divider ── */
hr {{
    border-color: {BORDER_COLOR} !important;
    opacity: 0.4 !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: {BG_DARK};
}}
::-webkit-scrollbar-thumb {{
    background: {SURFACE_3};
    border-radius: 3px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {PRIMARY_EMERALD};
}}
</style>
"""


# ══════════════════════════════════════════════════════════════════
# PUBLIC HELPERS
# ══════════════════════════════════════════════════════════════════

def inject_css() -> None:
    """
    Injects the full glass-morphism CSS into the Streamlit page.
    Call once at the top of app.py after st.set_page_config().
    """
    st.markdown(GLASSMORPHISM_CSS, unsafe_allow_html=True)


def get_color_scale() -> list:
    """
    Returns a continuous Emerald → Gold color scale for heatmaps.
    Compatible with Plotly's color_continuous_scale parameter.
    """
    return [
        [0.0, SURFACE_2],        # Dark base (low values)
        [0.5, PRIMARY_EMERALD],  # Emerald midpoint
        [1.0, ACCENT_GOLD]       # Gold peak (high values)
    ]


def status_badge(label: str, status: str = "default") -> str:
    """
    Generates an inline HTML badge for use in st.markdown().
    
    Args:
        label: Badge text
        status: 'success' | 'warning' | 'danger' | 'info' | 'default'
        
    Returns:
        HTML string for a colored pill badge
        
    Example:
        st.markdown(status_badge("Closed Won", "success"), unsafe_allow_html=True)
    """
    color_map = {
        "success": (SUCCESS_GREEN,   "rgba(16,185,129,0.15)"),
        "warning": (WARNING_AMBER,   "rgba(245,158,11,0.15)"),
        "danger":  (DANGER_RED,      "rgba(220,38,38,0.15)"),
        "info":    (INFO_BLUE,       "rgba(59,130,246,0.15)"),
        "default": (PRIMARY_EMERALD, GLASS_BG),
    }
    text_color, bg_color = color_map.get(status, color_map["default"])
    return (
        f'<span style="'
        f'background:{bg_color};'
        f'color:{text_color};'
        f'border:1px solid {text_color};'
        f'border-radius:20px;'
        f'padding:3px 12px;'
        f'font-size:0.75rem;'
        f'font-weight:600;'
        f'letter-spacing:0.05em;'
        f'font-family:Inter,sans-serif;'
        f'">{label}</span>'
    )


def section_header(title: str, subtitle: str = "") -> None:
    """
    Renders a branded section header with optional subtitle.
    
    Args:
        title: Bold header text
        subtitle: Dimmed caption below (optional)
    """
    st.markdown(
        f"""
        <div style="margin-bottom:1rem;">
            <h3 style="
                color:{TEXT_PRIMARY};
                font-family:Inter,sans-serif;
                font-weight:700;
                font-size:1.3rem;
                margin:0 0 4px 0;
                letter-spacing:-0.01em;
            ">{title}</h3>
            {"" if not subtitle else f'<p style="color:{TEXT_SECONDARY};font-size:0.85rem;margin:0;">{subtitle}</p>'}
        </div>
        """,
        unsafe_allow_html=True
    )


# ── Initialize template on import ──
apply_custom_theme()
