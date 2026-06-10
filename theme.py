"""
theme.py - Premium Visual Identity for Sales Intel Terminal v2.0

Defines:
- Emerald + Gold branded color palette (3-layer depth system)
- Dual-font system: Space Grotesk (headings) + JetBrains Mono (values)
- Plotly 'sales_intel_dark' custom template
- Premium glass-morphism CSS with glow effects + fadeInUp animations
- Helper utilities: section_header, status_badge, pulse_dot, kpi_card, export_bar
"""

import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

# ══════════════════════════════════════════════════════════════════
# COLOR PALETTE — Emerald + Gold (3-Layer Depth System)
# ══════════════════════════════════════════════════════════════════

# Primary Brand
PRIMARY_EMERALD   = "#059669"   # Deep Emerald — primary brand, main KPIs
ACCENT_GOLD       = "#FBBF24"   # Gold — success, closed deals, premium highlights
SECONDARY_TEAL    = "#0D9488"   # Teal — secondary charts, supporting data
EMERALD_BRIGHT    = "#34D399"   # Bright Emerald — glow accents, active states

# Status Colors
SUCCESS_GREEN     = "#10B981"   # Positive trends, growth indicators
WARNING_AMBER     = "#F59E0B"   # At-risk, slow stages
DANGER_RED        = "#EF4444"   # Negative deltas, drop-offs, alerts
INFO_BLUE         = "#3B82F6"   # Neutral information, tooltips

# ── 3-Layer Depth System ──
BG_DARK           = "#060C09"   # Layer 0: Page background (deepest)
SURFACE_1         = "#0D1510"   # Layer 1: Main card surface
SURFACE_2         = "#142018"   # Layer 2: Inner panels, sidebar
SURFACE_3         = "#1C2E22"   # Layer 3: Hover states, nested cells
SURFACE_4         = "#243A2C"   # Layer 4: Active/selected elements

# Borders
BORDER_SUBTLE     = "#1E3328"   # Barely-visible structural border
BORDER_COLOR      = "#2D4A3A"   # Standard card border
BORDER_ACTIVE     = "#3D6B52"   # Active/focused border
BORDER_GLOW       = "#059669"   # Hover glow border (Emerald)

# Text
TEXT_PRIMARY      = "#F0FDF4"   # Main text (near-white with green tint)
TEXT_SECONDARY    = "#86EFAC"   # Dimmed labels (light green)
TEXT_MUTED        = "#4ADE80"   # Placeholders (muted green)
TEXT_DIM          = "#374151"   # Very dim — decorative only

# Glass-morphism Layer
GLASS_BG          = "rgba(5, 150, 105, 0.05)"
GLASS_BG_HOVER    = "rgba(5, 150, 105, 0.10)"
GLASS_BORDER      = "rgba(5, 150, 105, 0.20)"
GLASS_BORDER_HOVER= "rgba(52, 211, 153, 0.45)"
GLASS_BLUR        = "blur(16px)"
GLASS_SHADOW      = "0 4px 24px rgba(0,0,0,0.4), 0 1px 0 rgba(5,150,105,0.1)"
GLASS_SHADOW_HOVER= "0 8px 40px rgba(0,0,0,0.5), 0 0 20px rgba(5,150,105,0.2)"

# Glow Effects
GLOW_SM           = "0 0 12px rgba(5, 150, 105, 0.35)"
GLOW_MD           = "0 0 24px rgba(5, 150, 105, 0.45)"
GLOW_LG           = "0 0 40px rgba(5, 150, 105, 0.55)"
TEXT_GLOW         = "0 0 10px rgba(52, 211, 153, 0.5)"

# Color sequence for multi-series charts
CHART_COLOR_SEQUENCE = [
    PRIMARY_EMERALD,
    ACCENT_GOLD,
    SECONDARY_TEAL,
    EMERALD_BRIGHT,
    WARNING_AMBER,
    INFO_BLUE,
    DANGER_RED,
]


# ══════════════════════════════════════════════════════════════════
# PLOTLY TEMPLATE — sales_intel_dark
# ══════════════════════════════════════════════════════════════════

def apply_custom_theme() -> None:
    """
    Builds and registers the 'sales_intel_dark' Plotly template globally.
    Call once at app startup in app.py before any chart rendering.
    Uses JetBrains Mono for tick labels, Space Grotesk for titles.
    """
    template = go.layout.Template()

    template.layout = go.Layout(
        plot_bgcolor  = "rgba(0,0,0,0)",
        paper_bgcolor = "rgba(0,0,0,0)",

        font=dict(
            family = "JetBrains Mono, monospace",
            color  = TEXT_SECONDARY,
            size   = 11
        ),

        title=dict(
            font=dict(
                family = "Space Grotesk, system-ui, sans-serif",
                size   = 16,
                color  = TEXT_PRIMARY
            ),
            x        = 0.0,
            xanchor  = "left",
            pad      = dict(l=4)
        ),

        xaxis=dict(
            gridcolor       = SURFACE_3,
            zerolinecolor   = SURFACE_3,
            linecolor       = BORDER_COLOR,
            tickfont        = dict(
                family = "JetBrains Mono, monospace",
                color  = TEXT_SECONDARY,
                size   = 10
            ),
            showgrid        = True,
            showline        = True,
            zeroline        = False,
            ticklen         = 4,
            tickcolor       = BORDER_COLOR,
        ),
        yaxis=dict(
            gridcolor       = SURFACE_3,
            zerolinecolor   = SURFACE_3,
            linecolor       = BORDER_COLOR,
            tickfont        = dict(
                family = "JetBrains Mono, monospace",
                color  = TEXT_SECONDARY,
                size   = 10
            ),
            showgrid        = True,
            showline        = True,
            zeroline        = False,
            ticklen         = 4,
            tickcolor       = BORDER_COLOR,
        ),

        legend=dict(
            orientation  = "h",
            yanchor      = "bottom",
            y            = 1.02,
            xanchor      = "right",
            x            = 1,
            font         = dict(
                family = "JetBrains Mono, monospace",
                color  = TEXT_SECONDARY,
                size   = 10
            ),
            bgcolor      = "rgba(0,0,0,0)",
            bordercolor  = BORDER_COLOR,
            borderwidth  = 1
        ),

        hoverlabel=dict(
            bgcolor     = SURFACE_2,
            bordercolor = EMERALD_BRIGHT,
            font        = dict(
                family = "JetBrains Mono, monospace",
                size   = 11,
                color  = TEXT_PRIMARY
            )
        ),

        margin   = dict(t=50, b=44, l=48, r=24),
        colorway = CHART_COLOR_SEQUENCE
    )

    pio.templates["sales_intel_dark"] = template
    pio.templates.default             = "sales_intel_dark"


# ══════════════════════════════════════════════════════════════════
# PREMIUM CSS — Glass-morphism v2 + Glow + Animations + Fonts
# ══════════════════════════════════════════════════════════════════

GLASSMORPHISM_CSS = f"""
<style>

/* ══════════════════════════════════════════
   FONT IMPORTS
══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');

/* ══════════════════════════════════════════
   GLOBAL RESET
══════════════════════════════════════════ */
html, body, [class*="css"] {{
    font-family: 'Space Grotesk', system-ui, sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    text-rendering: optimizeLegibility !important;
}}

/* ══════════════════════════════════════════
   KEYFRAME ANIMATIONS
══════════════════════════════════════════ */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to   {{ opacity: 1; transform: translateY(0);    }}
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}

@keyframes pulse-glow {{
    0%, 100% {{ box-shadow: 0 0 6px rgba(5,150,105,0.4);  }}
    50%        {{ box-shadow: 0 0 18px rgba(5,150,105,0.8); }}
}}

@keyframes pulse-dot {{
    0%, 100% {{ opacity: 1;   transform: scale(1);   }}
    50%        {{ opacity: 0.5; transform: scale(1.3); }}
}}

@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}

@keyframes borderGlow {{
    0%, 100% {{ border-color: rgba(5,150,105,0.2); }}
    50%        {{ border-color: rgba(52,211,153,0.5); }}
}}

/* ══════════════════════════════════════════
   PAGE BACKGROUND — Deep radial mesh
══════════════════════════════════════════ */
.stApp {{
    background:
        radial-gradient(ellipse at 20% 20%, rgba(5,150,105,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(13,148,136,0.05) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(6,12,9,1) 0%, {BG_DARK} 100%)
        !important;
    background-attachment: fixed !important;
    min-height: 100vh !important;
}}

/* ══════════════════════════════════════════
   MAIN CONTENT AREA
══════════════════════════════════════════ */
.main .block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1400px !important;
    animation: fadeIn 0.5s ease !important;
}}

/* ══════════════════════════════════════════
   GLASS CARD — Base Component
══════════════════════════════════════════ */
.glass-card {{
    background    : {GLASS_BG} !important;
    backdrop-filter: {GLASS_BLUR} !important;
    -webkit-backdrop-filter: {GLASS_BLUR} !important;
    border        : 1px solid {GLASS_BORDER} !important;
    border-radius : 16px !important;
    box-shadow    : {GLASS_SHADOW} !important;
    padding       : 1.5rem !important;
    transition    : all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    animation     : fadeInUp 0.4s ease !important;
    position      : relative !important;
    overflow      : hidden !important;
}}

/* Subtle top-edge highlight line */
.glass-card::before {{
    content  : '';
    position : absolute;
    top      : 0; left : 0; right: 0;
    height   : 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(52,211,153,0.4),
        transparent
    );
}}

.glass-card:hover {{
    background    : {GLASS_BG_HOVER} !important;
    border-color  : {GLASS_BORDER_HOVER} !important;
    box-shadow    : {GLASS_SHADOW_HOVER} !important;
    transform     : translateY(-3px) !important;
}}

/* ══════════════════════════════════════════
   KPI METRIC CARDS
══════════════════════════════════════════ */
[data-testid="metric-container"] {{
    background      : {GLASS_BG} !important;
    backdrop-filter : {GLASS_BLUR} !important;
    -webkit-backdrop-filter: {GLASS_BLUR} !important;
    border          : 1px solid {GLASS_BORDER} !important;
    border-radius   : 14px !important;
    box-shadow      : {GLASS_SHADOW} !important;
    padding         : 1.2rem 1.4rem !important;
    transition      : all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    animation       : fadeInUp 0.4s ease !important;
    position        : relative !important;
    overflow        : hidden !important;
}}

/* Shimmer highlight on top edge */
[data-testid="metric-container"]::before {{
    content  : '';
    position : absolute;
    top: 0; left: 0; right: 0;
    height   : 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(52,211,153,0.5),
        transparent
    );
}}

[data-testid="metric-container"]:hover {{
    border-color : rgba(52,211,153,0.45) !important;
    box-shadow   : {GLASS_SHADOW_HOVER} !important;
    transform    : translateY(-3px) !important;
    background   : {GLASS_BG_HOVER} !important;
}}

/* Metric VALUE — JetBrains Mono, Gold */
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    font-family : 'JetBrains Mono', monospace !important;
    color       : {ACCENT_GOLD} !important;
    font-size   : 2rem !important;
    font-weight : 700 !important;
    letter-spacing: -0.02em !important;
    text-shadow : 0 0 20px rgba(251,191,36,0.3) !important;
}}

/* Metric LABEL — Space Grotesk, ALL CAPS */
[data-testid="metric-container"] [data-testid="stMetricLabel"] {{
    font-family    : 'Space Grotesk', sans-serif !important;
    color          : {TEXT_SECONDARY} !important;
    font-size      : 0.7rem !important;
    font-weight    : 600 !important;
    text-transform : uppercase !important;
    letter-spacing : 0.1em !important;
}}

/* Metric DELTA */
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-family : 'JetBrains Mono', monospace !important;
    font-size   : 0.8rem !important;
    font-weight : 600 !important;
}}

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
[data-testid="stSidebar"] {{
    background: linear-gradient(
        180deg,
        {SURFACE_1} 0%,
        {SURFACE_2} 60%,
        {BG_DARK}   100%
    ) !important;
    border-right : 1px solid {GLASS_BORDER} !important;
    box-shadow   : 4px 0 24px rgba(0,0,0,0.4) !important;
}}

/* Sidebar section labels */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] .stSlider label {{
    font-family    : 'JetBrains Mono', monospace !important;
    color          : {TEXT_SECONDARY} !important;
    font-size      : 0.7rem !important;
    text-transform : uppercase !important;
    letter-spacing : 0.1em !important;
    font-weight    : 500 !important;
}}

/* Sidebar caption text */
[data-testid="stSidebar"] .stCaption p {{
    font-family : 'JetBrains Mono', monospace !important;
    color       : {TEXT_MUTED} !important;
    font-size   : 0.65rem !important;
}}

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {{
    background    : {SURFACE_1} !important;
    border-radius : 14px !important;
    padding       : 5px !important;
    gap           : 4px !important;
    border        : 1px solid {GLASS_BORDER} !important;
    box-shadow    : inset 0 1px 0 rgba(255,255,255,0.03) !important;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius  : 10px !important;
    color          : {TEXT_SECONDARY} !important;
    font-family    : 'Space Grotesk', sans-serif !important;
    font-weight    : 500 !important;
    font-size      : 0.85rem !important;
    letter-spacing : 0.02em !important;
    transition     : all 0.2s ease !important;
    padding        : 0.55rem 1.4rem !important;
}}

.stTabs [data-baseweb="tab"]:hover {{
    color      : {TEXT_PRIMARY} !important;
    background : {SURFACE_3} !important;
}}

.stTabs [aria-selected="true"] {{
    background  : linear-gradient(135deg, {PRIMARY_EMERALD} 0%, {SECONDARY_TEAL} 100%) !important;
    color       : {TEXT_PRIMARY} !important;
    font-weight : 700 !important;
    box-shadow  : {GLOW_SM} !important;
}}

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
.stButton > button {{
    font-family    : 'Space Grotesk', sans-serif !important;
    background     : linear-gradient(135deg, {PRIMARY_EMERALD} 0%, {SECONDARY_TEAL} 100%) !important;
    color          : {TEXT_PRIMARY} !important;
    border         : none !important;
    border-radius  : 10px !important;
    font-weight    : 700 !important;
    font-size      : 0.85rem !important;
    letter-spacing : 0.05em !important;
    text-transform : uppercase !important;
    padding        : 0.6rem 1.5rem !important;
    transition     : all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
    position       : relative !important;
    overflow       : hidden !important;
}}

.stButton > button::after {{
    content    : '';
    position   : absolute;
    inset      : 0;
    background : linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
    opacity    : 0;
    transition : opacity 0.2s ease;
}}

.stButton > button:hover {{
    transform  : translateY(-2px) !important;
    box-shadow : {GLOW_MD} !important;
}}

.stButton > button:hover::after {{
    opacity: 1 !important;
}}

.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* Download button variant */
[data-testid="stDownloadButton"] > button {{
    font-family    : 'JetBrains Mono', monospace !important;
    background     : transparent !important;
    color          : {TEXT_SECONDARY} !important;
    border         : 1px solid {BORDER_COLOR} !important;
    border-radius  : 8px !important;
    font-size      : 0.75rem !important;
    text-transform : uppercase !important;
    letter-spacing : 0.08em !important;
    transition     : all 0.2s ease !important;
}}

[data-testid="stDownloadButton"] > button:hover {{
    border-color : {PRIMARY_EMERALD} !important;
    color        : {PRIMARY_EMERALD} !important;
    box-shadow   : {GLOW_SM} !important;
    transform    : translateY(-1px) !important;
}}

/* ══════════════════════════════════════════
   INPUT FIELDS
══════════════════════════════════════════ */
.stTextInput > div > div > input {{
    font-family  : 'JetBrains Mono', monospace !important;
    background   : {SURFACE_2} !important;
    border       : 1px solid {BORDER_COLOR} !important;
    border-radius: 10px !important;
    color        : {TEXT_PRIMARY} !important;
    font-size    : 0.9rem !important;
    transition   : all 0.2s ease !important;
    caret-color  : {PRIMARY_EMERALD} !important;
}}

.stTextInput > div > div > input:focus {{
    border-color : {PRIMARY_EMERALD} !important;
    box-shadow   : 0 0 0 3px rgba(5,150,105,0.15), {GLOW_SM} !important;
    outline      : none !important;
}}

.stTextInput > div > div > input::placeholder {{
    color: {TEXT_DIM} !important;
}}

/* Selectbox + Multiselect */
.stSelectbox > div > div,
.stMultiSelect > div > div {{
    background    : {SURFACE_2} !important;
    border        : 1px solid {BORDER_COLOR} !important;
    border-radius : 10px !important;
    color         : {TEXT_PRIMARY} !important;
    transition    : all 0.2s ease !important;
}}

.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within {{
    border-color : {PRIMARY_EMERALD} !important;
    box-shadow   : {GLOW_SM} !important;
}}

/* ══════════════════════════════════════════
   DATAFRAMES / TABLES
══════════════════════════════════════════ */
[data-testid="stDataFrame"] {{
    background    : {GLASS_BG} !important;
    border        : 1px solid {GLASS_BORDER} !important;
    border-radius : 14px !important;
    overflow      : hidden !important;
    box-shadow    : {GLASS_SHADOW} !important;
    animation     : fadeInUp 0.4s ease !important;
}}

[data-testid="stDataFrame"] table {{
    font-family : 'JetBrains Mono', monospace !important;
    font-size   : 0.82rem !important;
}}

[data-testid="stDataFrame"] th {{
    background     : {SURFACE_2} !important;
    color          : {TEXT_SECONDARY} !important;
    font-family    : 'Space Grotesk', sans-serif !important;
    font-size      : 0.7rem !important;
    text-transform : uppercase !important;
    letter-spacing : 0.08em !important;
    border-bottom  : 1px solid {BORDER_COLOR} !important;
    font-weight    : 600 !important;
}}

/* ══════════════════════════════════════════
   PLOTLY CHART CONTAINERS
══════════════════════════════════════════ */
[data-testid="stPlotlyChart"] {{
    background      : {GLASS_BG} !important;
    backdrop-filter : {GLASS_BLUR} !important;
    border          : 1px solid {GLASS_BORDER} !important;
    border-radius   : 16px !important;
    padding         : 0.75rem !important;
    box-shadow      : {GLASS_SHADOW} !important;
    transition      : all 0.25s ease !important;
    animation       : fadeInUp 0.45s ease !important;
}}

[data-testid="stPlotlyChart"]:hover {{
    border-color : {GLASS_BORDER_HOVER} !important;
    box-shadow   : {GLASS_SHADOW_HOVER} !important;
}}

/* ══════════════════════════════════════════
   ALERTS / INFO BOXES
══════════════════════════════════════════ */
.stAlert {{
    background      : {GLASS_BG} !important;
    border          : 1px solid {GLASS_BORDER} !important;
    border-radius   : 12px !important;
    backdrop-filter : {GLASS_BLUR} !important;
    font-family     : 'JetBrains Mono', monospace !important;
    font-size       : 0.82rem !important;
}}

/* ══════════════════════════════════════════
   SPINNER
══════════════════════════════════════════ */
[data-testid="stSpinner"] {{
    color: {PRIMARY_EMERALD} !important;
}}

/* ══════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════ */
[data-testid="stExpander"] {{
    background    : {GLASS_BG} !important;
    border        : 1px solid {GLASS_BORDER} !important;
    border-radius : 12px !important;
    transition    : all 0.2s ease !important;
}}

[data-testid="stExpander"]:hover {{
    border-color : {BORDER_ACTIVE} !important;
}}

[data-testid="stExpander"] summary {{
    font-family    : 'Space Grotesk', sans-serif !important;
    font-weight    : 600 !important;
    color          : {TEXT_PRIMARY} !important;
    text-transform : uppercase !important;
    letter-spacing : 0.06em !important;
    font-size      : 0.82rem !important;
}}

/* ══════════════════════════════════════════
   DIVIDER
══════════════════════════════════════════ */
hr {{
    border  : none !important;
    height  : 1px !important;
    background: linear-gradient(90deg,
        transparent,
        {BORDER_COLOR},
        transparent
    ) !important;
    opacity : 0.6 !important;
    margin  : 1.5rem 0 !important;
}}

/* ══════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar        {{ width: 5px; height: 5px; }}
::-webkit-scrollbar-track {{ background: {BG_DARK}; }}
::-webkit-scrollbar-thumb {{
    background    : {SURFACE_3};
    border-radius : 3px;
    transition    : background 0.2s ease;
}}
::-webkit-scrollbar-thumb:hover {{ background: {PRIMARY_EMERALD}; }}

/* ══════════════════════════════════════════
   PULSE DOT (live status indicator)
══════════════════════════════════════════ */
.pulse-dot {{
    display      : inline-block;
    width        : 8px;
    height       : 8px;
    border-radius: 50%;
    background   : {SUCCESS_GREEN};
    animation    : pulse-dot 2s ease-in-out infinite;
    margin-right : 6px;
    box-shadow   : 0 0 6px {SUCCESS_GREEN};
}}

.pulse-dot.warning  {{ background: {WARNING_AMBER}; box-shadow: 0 0 6px {WARNING_AMBER}; }}
.pulse-dot.danger   {{ background: {DANGER_RED};    box-shadow: 0 0 6px {DANGER_RED};    }}

/* ══════════════════════════════════════════
   HEADER BAR (used in app.py render_header)
══════════════════════════════════════════ */
.header-bar {{
    display         : flex;
    align-items     : center;
    justify-content : space-between;
    background      : {GLASS_BG};
    backdrop-filter : {GLASS_BLUR};
    border          : 1px solid {GLASS_BORDER};
    border-radius   : 16px;
    padding         : 0.85rem 1.5rem;
    margin-bottom   : 1.5rem;
    box-shadow      : {GLASS_SHADOW};
    animation       : fadeInUp 0.3s ease;
}}

.header-bar .brand {{
    font-family    : 'Space Grotesk', sans-serif;
    font-size      : 1.1rem;
    font-weight    : 800;
    color          : {TEXT_PRIMARY};
    letter-spacing : -0.02em;
}}

.header-bar .brand span {{
    color      : {PRIMARY_EMERALD};
    text-shadow: {TEXT_GLOW};
}}

.header-bar .meta {{
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.72rem;
    color          : {TEXT_SECONDARY};
    letter-spacing : 0.06em;
    display        : flex;
    align-items    : center;
    gap            : 1.2rem;
}}

/* ══════════════════════════════════════════
   EXPORT BAR (used in views.py)
══════════════════════════════════════════ */
.export-bar {{
    display         : flex;
    align-items     : center;
    gap             : 0.75rem;
    padding         : 0.65rem 1rem;
    background      : {GLASS_BG};
    border          : 1px solid {GLASS_BORDER};
    border-radius   : 10px;
    margin-bottom   : 1.25rem;
    animation       : fadeInUp 0.35s ease;
}}

.export-bar .export-label {{
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.68rem;
    color          : {TEXT_SECONDARY};
    text-transform : uppercase;
    letter-spacing : 0.12em;
    margin-right   : auto;
}}

/* ══════════════════════════════════════════
   SECTION HEADER
══════════════════════════════════════════ */
.section-header {{
    border-left    : 3px solid {PRIMARY_EMERALD};
    padding-left   : 0.85rem;
    margin-bottom  : 1.2rem;
    animation      : fadeInUp 0.35s ease;
}}

.section-header h3 {{
    font-family    : 'Space Grotesk', sans-serif;
    font-size      : 1.1rem;
    font-weight    : 700;
    color          : {TEXT_PRIMARY};
    margin         : 0 0 2px 0;
    letter-spacing : -0.02em;
}}

.section-header p {{
    font-family    : 'JetBrains Mono', monospace;
    font-size      : 0.7rem;
    color          : {TEXT_SECONDARY};
    margin         : 0;
    letter-spacing : 0.04em;
}}

</style>
"""


# ══════════════════════════════════════════════════════════════════
# PUBLIC HELPERS
# ══════════════════════════════════════════════════════════════════

def inject_css() -> None:
    """Injects premium glass-morphism CSS. Call once in app.py."""
    st.markdown(GLASSMORPHISM_CSS, unsafe_allow_html=True)


def get_color_scale() -> list:
    """Emerald → Gold continuous scale for Plotly heatmaps."""
    return [
        [0.0, SURFACE_2],
        [0.4, PRIMARY_EMERALD],
        [1.0, ACCENT_GOLD]
    ]


def status_badge(label: str, status: str = "default") -> str:
    """
    Inline HTML pill badge.
    status: 'success' | 'warning' | 'danger' | 'info' | 'default'
    """
    color_map = {
        "success": (SUCCESS_GREEN,  "rgba(16,185,129,0.12)"),
        "warning": (WARNING_AMBER,  "rgba(245,158,11,0.12)"),
        "danger":  (DANGER_RED,     "rgba(239,68,68,0.12)"),
        "info":    (INFO_BLUE,      "rgba(59,130,246,0.12)"),
        "default": (EMERALD_BRIGHT, "rgba(52,211,153,0.08)"),
    }
    fg, bg = color_map.get(status, color_map["default"])
    return (
        f'<span style="'
        f'background:{bg};color:{fg};border:1px solid {fg};'
        f'border-radius:20px;padding:2px 10px;'
        f'font-family:JetBrains Mono,monospace;'
        f'font-size:0.68rem;font-weight:600;letter-spacing:0.08em;'
        f'text-transform:uppercase;'
        f'">{label}</span>'
    )


def pulse_dot(status: str = "success") -> str:
    """Animated live-status dot. status: 'success'|'warning'|'danger'"""
    css_class = {"success": "", "warning": " warning", "danger": " danger"}.get(status, "")
    return f'<span class="pulse-dot{css_class}"></span>'


def section_header(title: str, subtitle: str = "") -> None:
    """
    Renders a branded section header with left Emerald accent bar.
    Uses Space Grotesk (title) + JetBrains Mono (subtitle).
    """
    sub_html = (
        f'<p style="font-family:JetBrains Mono,monospace;'
        f'font-size:0.7rem;color:{TEXT_SECONDARY};'
        f'margin:0;letter-spacing:0.04em;">{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(
        f"""
        <div class="section-header">
            <h3>{title}</h3>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_header(records: int = 0, username: str = "") -> None:
    """
    Renders the sticky branded top header bar.
    Shows brand name, live status dot, record count, and user.
    Call at the top of main() in app.py after data is loaded.
    """
    rec_str  = f"{records:,} records" if records else "no data"
    user_str = f"👤 {username.upper()}" if username else ""
    st.markdown(
        f"""
        <div class="header-bar">
            <div class="brand">
                📊 SALES INTEL <span>TERMINAL</span>
            </div>
            <div class="meta">
                {pulse_dot("success")} LIVE
                &nbsp;·&nbsp;
                <span style="font-family:JetBrains Mono,monospace;">
                    {rec_str}
                </span>
                &nbsp;·&nbsp;
                <span style="color:{ACCENT_GOLD};">{user_str}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def export_bar(df_csv: bytes, filename: str = "export.csv") -> None:
    """
    Renders a minimal export strip with CSV download button.
    Place at the top of each view in views.py.
    """
    st.markdown(
        '<div class="export-bar">'
        f'<span class="export-label">⬇ Export</span>',
        unsafe_allow_html=True
    )
    st.download_button(
        label="Download CSV",
        data=df_csv,
        file_name=filename,
        mime="text/csv",
        key=f"export_{filename}"
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ── Initialize Plotly template on import ──
apply_custom_theme()
