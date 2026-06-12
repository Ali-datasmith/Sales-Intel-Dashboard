"""
login.py - Authentication UI for Sales Intel Terminal v2.0

Emerald + Gold glass-morphism theme with scanline animation.
Single-user login backed by credentials.py (sha256, no plain text visible).

Functions:
    render_login()         → Full-page login screen
    render_logout_button() → Compact sidebar logout widget
"""

import streamlit as st
from credentials import validate_credentials, get_display_name, get_role

# ── Theme tokens (inline to avoid circular import with theme.py) ──
_EMERALD      = "#059669"
_EMERALD_DIM  = "rgba(5,150,105,0.20)"
_EMERALD_GLOW = "rgba(5,150,105,0.35)"
_GOLD         = "#FBBF24"
_BG           = "#060C09"
_SURFACE      = "#0D1510"
_SURFACE2     = "#142018"
_BORDER       = "rgba(5,150,105,0.22)"
_BORDER_FOCUS = "rgba(5,150,105,0.65)"
_TEXT         = "#F0FDF4"
_TEXT_DIM     = "rgba(134,239,172,0.55)"
_TEXT_MUTED   = "rgba(74,222,128,0.30)"
_RED          = "#EF4444"
_RED_DIM      = "rgba(239,68,68,0.12)"


def _inject_login_css() -> None:
    st.markdown(
        f"""
        <style>

        /* ── Fonts ── */
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'JetBrains Mono', monospace !important;
            -webkit-font-smoothing: antialiased !important;
        }}

        /* ── Background — deep Emerald radial mesh ── */
        .stApp {{
            background:
                radial-gradient(ellipse at  8%  25%, rgba(5,150,105,0.14)  0%, transparent 45%),
                radial-gradient(ellipse at 92%  10%, rgba(13,148,136,0.12)  0%, transparent 40%),
                radial-gradient(ellipse at 50%  90%, rgba(5,150,105,0.08)  0%, transparent 45%),
                radial-gradient(ellipse at 75%  55%, rgba(4,120,87,0.09)   0%, transparent 40%),
                linear-gradient(145deg, #040C07 0%, #060E09 40%, #050A07 100%)
                !important;
            background-attachment: fixed !important;
        }}

        /* ── Hide Streamlit chrome ── */
        #MainMenu, footer, header {{ visibility: hidden !important; }}
        .block-container {{ padding-top: 0 !important; }}

        /* ── Scanline sweep animation ── */
        @keyframes scanline {{
            0%   {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(100vh); }}
        }}
        .scanline {{
            position   : fixed;
            top        : 0; left: 0; right: 0;
            height     : 2px;
            background : linear-gradient(90deg,
                transparent,
                rgba(5,150,105,0.12),
                rgba(52,211,153,0.08),
                transparent
            );
            animation      : scanline 7s linear infinite;
            pointer-events : none;
            z-index        : 9999;
        }}

        /* ── Glassmorphism login card ── */
        .login-glass-card {{
            background     : rgba(5,150,105,0.04) !important;
            border         : 1px solid {_BORDER} !important;
            border-radius   : 22px;
            padding        : 52px 44px 44px 44px;
            backdrop-filter : blur(28px) saturate(160%) brightness(1.08);
            -webkit-backdrop-filter: blur(28px) saturate(160%) brightness(1.08);
            box-shadow     :
                0 8px 48px rgba(0,0,0,0.55),
                0 0 0 1px rgba(255,255,255,0.04) inset,
                0 1px 0   rgba(52,211,153,0.12) inset,
                0 0 80px  rgba(5,150,105,0.06);
            position: relative;
            overflow: hidden;
        }}

        /* Top shimmer line */
        .login-glass-card::before {{
            content    : '';
            position   : absolute;
            top: 0; left: 0; right: 0;
            height     : 1px;
            background : linear-gradient(90deg,
                transparent,
                rgba(52,211,153,0.5),
                transparent
            );
        }}

        /* ── Logo / title ── */
        .login-icon {{
            font-size    : 52px;
            text-align   : center;
            margin-bottom: 10px;
            filter       : drop-shadow(0 0 16px rgba(5,150,105,0.7));
        }}
        .login-title {{
            text-align   : center;
            color        : {_TEXT} !important;
            font-family  : 'Space Grotesk', sans-serif !important;
            font-size    : 1.9rem;
            font-weight  : 800;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }}
        .login-title span {{
            color      : {_EMERALD};
            text-shadow: 0 0 28px rgba(5,150,105,0.55),
                       0 0 56px rgba(5,150,105,0.25);
        }}
        .login-subtitle {{
            text-align    : center;
            color         : {_TEXT_DIM} !important;
            font-family   : 'JetBrains Mono', monospace !important;
            font-size     : 0.68rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom : 40px;
        }}

        /* ── Divider ── */
        .login-divider {{
            height     : 1px;
            background : linear-gradient(90deg,
                transparent,
                {_EMERALD_DIM},
                rgba(52,211,153,0.3),
                {_EMERALD_DIM},
                transparent
            );
            margin-bottom: 36px;
        }}

        /* ── Input labels ── */
        .stTextInput label {{
            color        : {_TEXT_DIM} !important;
            font-family   : 'JetBrains Mono', monospace !important;
            font-size     : 0.68rem !important;
            font-weight   : 600 !important;
            letter-spacing : 0.14em !important;
            text-transform : uppercase !important;
        }}

        /* ── Input fields ── */
        .stTextInput input {{
            background     : rgba(5,20,12,0.75) !important;
            border         : 1px solid {_BORDER} !important;
            border-radius   : 10px !important;
            color          : {_TEXT} !important;
            font-family     : 'JetBrains Mono', monospace !important;
            font-size       : 0.9rem !important;
            padding        : 14px 16px !important;
            transition     : all 0.25s ease !important;
            caret-color    : {_EMERALD} !important;
        }}
        .stTextInput input:focus {{
            border-color : {_BORDER_FOCUS} !important;
            box-shadow   :
                0 0 0 3px rgba(5,150,105,0.15),
                0 0 24px rgba(5,150,105,0.18) !important;
            background   : rgba(5,150,105,0.04) !important;
            outline      : none !important;
        }}
        .stTextInput input::placeholder {{
            color: {_TEXT_MUTED} !important;
        }}

        /* ── Hide "Press Enter" helper ── */
        .stTextInput div[data-testid="InputInstructions"],
        .stTextInput small,
        small[data-testid="InputInstructions"] {{
            display: none !important;
        }}

        /* ── Auth button ── */
        .stButton > button,
        .stFormSubmitButton > button {{
            width        : 100% !important;
            background     : linear-gradient(135deg,
                rgba(5,150,105,0.18),
                rgba(13,148,136,0.12)
            ) !important;
            border         : 1px solid rgba(5,150,105,0.55) !important;
            color          : {_EMERALD} !important;
            font-family    : 'JetBrains Mono', monospace !important;
            font-weight    : 700 !important;
            font-size      : 0.82rem !important;
            letter-spacing : 0.16em !important;
            text-transform : uppercase !important;
            padding        : 15px 24px !important;
            border-radius  : 10px !important;
            transition     : all 0.25s ease !important;
            margin-top     : 8px !important;
        }}
        .stButton > button:hover,
        .stFormSubmitButton > button:hover {{
            background  : linear-gradient(135deg,
                rgba(5,150,105,0.30),
                rgba(13,148,136,0.22)
            ) !important;
            box-shadow  :
                0 0 32px rgba(5,150,105,0.38),
                0 4px 20px rgba(0,0,0,0.4) !important;
            transform   : translateY(-2px) !important;
            border-color: rgba(52,211,153,0.7) !important;
            color       : #34D399 !important;
        }}
        .stButton > button:active,
        .stFormSubmitButton > button:active {{
            transform: translateY(0) !important;
        }}

        /* ── Alerts ── */
        div[data-testid="stAlert"] {{
            border-radius   : 10px !important;
            backdrop-filter : blur(8px);
            font-family     : 'JetBrains Mono', monospace !important;
            font-size       : 0.8rem !important;
        }}

        /* ── Footer ── */
        .login-footer {{
            text-align    : center;
            margin-top    : 32px;
            font-family   : 'JetBrains Mono', monospace;
            font-size     : 0.62rem;
            color         : {_TEXT_MUTED} !important;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }}

        </style>

        <div class="scanline"></div>
        """,
        unsafe_allow_html=True,
    )


def render_login() -> None:
    """
    Renders the full-page glass-morphism login screen.

    On success:
        - Sets session_state: authenticated, username, display_name, role
        - st.balloons() celebration
        - st.rerun() to pass the login gate in app.py

    On failure:
        - Shows generic error (never reveals which field was wrong)
    """
    _inject_login_css()

    st.markdown("<div style='padding-top:60px;'></div>", unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.1, 1])

    with col:

        # ── Decorative card header (pure HTML — no inputs) ──
        st.markdown(
            f"""
            <div class="login-glass-card">
                <div class="login-icon">📊</div>
                <div class="login-title">
                    SALES INTEL <span>TERMINAL</span>
                </div>
                <div class="login-subtitle">
                    Secure Access Portal &nbsp;·&nbsp; v2.0
                </div>
                <div class="login-divider"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Login form (must be Streamlit — not raw HTML) ──
        with st.form("login_form", clear_on_submit=False):

            username = st.text_input(
                "Username",
                placeholder="Enter username",
                key="login_username_field",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password",
                key="login_password_field",
            )

            submitted = st.form_submit_button(
                "🚀  AUTHENTICATE",
                type="primary",
                use_container_width=True,
            )

            if submitted:
                is_valid, message = validate_credentials(username, password)

                if is_valid:
                    st.session_state["authenticated"] = True
                    st.session_state["username"]      = username.strip()
                    st.session_state["display_name"]  = get_display_name(username.strip())
                    st.session_state["role"]          = get_role(username.strip())
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"⛔  {message}")

        # ── Footer ──
        st.markdown(
            """
            <div class="login-footer">
                © 2026 Sales Intel Terminal &nbsp;|&nbsp; Ali-datasmith
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_logout_button() -> None:
    """
    Compact logout button for the sidebar.
    Clears all session state and reruns to show login screen.
    """
    if st.button(
        "Sign Out",
        key="logout_btn",
        use_container_width=True,
    ):
        _clear_session()
        st.rerun()


def _clear_session() -> None:
    """Wipes all session keys on logout."""
    for key in [
        "authenticated", "username", "display_name", "role",
        "df", "data_processed", "file_key",
    ]:
        st.session_state.pop(key, None)
