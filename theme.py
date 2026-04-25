"""
theme.py - Visual identity for SalesIntelDashboard.
Defines the Plotly dark-mode template and branded color palettes.
"""

import plotly.graph_objects as go
import plotly.io as pio

# Branded Color Palette
PRIMARY_ACCENT = "#00D4FF"  # Cyan for growth/positive
SECONDARY_ACCENT = "#7000FF" # Indigo for targets
DANGER = "#FF4B4B"           # Red for leakage/variance alerts
SUCCESS = "#00CC96"          # Green for closed deals
BACKGROUND_DARK = "#0E1117"  # Streamlit default dark
SURFACE_LIGHT = "#262730"    # Lighter grey for card-like contrast
TEXT_MAIN = "#FAFAFA"
TEXT_DIM = "#BFBFBF"

def apply_custom_theme():
    """
    Initializes and sets the global Plotly template for the application.
    """
    template = go.layout.Template()

    # Layout styling
    template.layout = go.Layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT_MAIN, size=12),
        title=dict(font=dict(size=18, color=TEXT_MAIN), x=0.05),
        margin=dict(t=60, b=40, l=40, r=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=TEXT_DIM)
        ),
        xaxis=dict(
            gridcolor="#333333",
            zerolinecolor="#333333",
            tickfont=dict(color=TEXT_DIM),
            showline=True,
            linecolor="#333333"
        ),
        yaxis=dict(
            gridcolor="#333333",
            zerolinecolor="#333333",
            tickfont=dict(color=TEXT_DIM),
            showline=True,
            linecolor="#333333"
        ),
        colorway=[PRIMARY_ACCENT, SECONDARY_ACCENT, SUCCESS, "#FFAA00", DANGER]
    )

    # Register and set as default
    pio.templates["sales_intel_dark"] = template
    pio.templates.default = "sales_intel_dark"

def get_color_scale():
    """Returns a continuous color scale for heatmaps/choropleths."""
    return [
        [0.0, BACKGROUND_DARK],
        [0.5, SECONDARY_ACCENT],
        [1.0, PRIMARY_ACCENT]
    ]

# Initialize on import
apply_custom_theme()
