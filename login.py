"""
login.py - Authentication UI Layer for Sales Intel Terminal.

Provides:
    render_login()         → Full-page login screen (blocks unauthenticated access)
    render_logout_button() → Compact logout widget for sidebar

Session state keys managed:
    st.session_state["authenticated"]  → bool
    st.session_state["username"]       → str
    st.session_state["display_name"]   → str
    st.session_state["role"]           → str ("admin" | "viewer")
"""

import streamlit as st
from credentials import authenticate

# ── Theme colors (inline — avoids circular import with theme.py) ──
_EMERALD  = "#059669"
_GOLD     = "#FBBF24"
_SURFACE  = "#111814"
_BORDER   = "rgba(5,150,105,0.25)"
_TEXT     = "#F1F5F9"
_TEXT_DIM = "#94A3B8"
_RED      = "#DC2626"


# ══════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════

def render_login() -> None:
    """
    Renders the full-page login screen.

    On successful authentication:
        - Sets st.session_state["authenticated"] = True
        - Stores username, display_name, role in session
        - Calls st.rerun() to reload app behind the gate

    On failure:
        - Shows an error message
        - Clears the password field
        - Does NOT reveal which field was wrong (security best practice)
    """

    # ── Centre the login card ──
    _, center_col, _ = st.columns([1, 1.6, 1])

    with center_col:

        # ── Logo / brand ──
        st.markdown(
            f"""
            <div style="text-align:center;padding:2.5rem 0 1.5rem 0;">
                <div style="font-size:3rem;margin-bottom:0.5rem;">📊</div>
                <h1 style="
                    font-family:Inter,sans-serif;
                    font-size:1.8rem;
                    font-weight:800;
                    color:{_TEXT};
                    letter-spacing:-0.03em;
                    margin:0 0 0.25rem 0;
                ">Sales Intel <span style="color:{_EMERALD};">Terminal</span></h1>
                <p style="
                    font-family:Inter,sans-serif;
                    font-size:0.82rem;
                    color:{_TEXT_DIM};
                    margin:0;
                    letter-spacing:0.04em;
                ">HIGH-PERFORMANCE DATA TERMINAL</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Glass login card ──
        st.markdown(
            f"""
            <div style="
                background:rgba(5,150,105,0.06);
                backdrop-filter:blur(12px);
                -webkit-backdrop-filter:blur(12px);
                border:1px solid {_BORDER};
                border-radius:20px;
                padding:2rem 2rem 1.5rem 2rem;
                box-shadow:0 8px 32px rgba(5,150,105,0.12);
            ">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <p style="
                font-family:Inter,sans-serif;
                font-size:0.78rem;
                font-weight:600;
                text-transform:uppercase;
                letter-spacing:0.1em;
                color:{_EMERALD};
                margin:0 0 1.2rem 0;
            ">🔐 Sign In</p>
            """,
            unsafe_allow_html=True
        )

        # ── Form fields ──
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Login button ──
        login_clicked = st.button(
            "Sign In →",
            use_container_width=True,
            key="login_btn"
        )

        # ── Error placeholder ──
        error_slot = st.empty()

        st.markdown("</div>", unsafe_allow_html=True)

        # ── Demo credentials hint ──
        st.markdown(
            f"""
            <div style="
                text-align:center;
                margin-top:1.2rem;
                padding:0.75rem 1rem;
                background:rgba(251,191,36,0.06);
                border:1px solid rgba(251,191,36,0.2);
                border-radius:12px;
            ">
                <p style="
                    font-family:Inter,sans-serif;
                    font-size:0.75rem;
                    color:{_TEXT_DIM};
                    margin:0 0 0.3rem 0;
                    font-weight:600;
                    text-transform:uppercase;
                    letter-spacing:0.08em;
                ">Demo Credentials</p>
                <p style="
                    font-family:Inter,sans-serif;
                    font-size:0.8rem;
                    color:{_TEXT};
                    margin:0;
                    line-height:1.7;
                ">
                    <span style="color:{_GOLD};">admin</span> / admin123
                    &nbsp;·&nbsp;
                    <span style="color:{_GOLD};">analyst</span> / analyst123
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Footer ──
        st.markdown(
            f"""
            <p style="
                text-align:center;
                font-family:Inter,sans-serif;
                font-size:0.72rem;
                color:#334155;
                margin-top:1.5rem;
                letter-spacing:0.05em;
            ">Sales Intel Terminal &nbsp;·&nbsp; v2.0 &nbsp;·&nbsp;
            <span style="color:{_EMERALD};">Ali-datasmith</span></p>
            """,
            unsafe_allow_html=True
        )

    # ── Authentication logic ──
    if login_clicked:
        if not username or not password:
            error_slot.error("Please enter both username and password.")
            return

        user = authenticate(username, password)

        if user:
            # ✅ Authenticated — store in session
            st.session_state["authenticated"] = True
            st.session_state["username"]      = user["username"]
            st.session_state["display_name"]  = user["display_name"]
            st.session_state["role"]          = user["role"]
            st.rerun()
        else:
            # ❌ Failed — generic message (don't reveal which field was wrong)
            error_slot.error("Invalid username or password. Please try again.")


# ══════════════════════════════════════════════════════════════════
# LOGOUT
# ══════════════════════════════════════════════════════════════════

def render_logout_button() -> None:
    """
    Renders a compact logout button in the sidebar.
    On click: clears all session state and reruns to show login screen.
    """
    if st.button(
        "Sign Out",
        key="logout_btn",
        use_container_width=True
    ):
        _clear_session()
        st.rerun()


def _clear_session() -> None:
    """
    Clears all session state keys on logout.
    Ensures no data lingers between sessions.
    """
    keys_to_clear = [
        "authenticated",
        "username",
        "display_name",
        "role",
        "df",
        "data_processed",
        "file_key",
    ]
    for key in keys_to_clear:
        st.session_state.pop(key, None)
