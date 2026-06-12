"""
credentials.py - User Authentication Store.

Single-user store. Credentials are hashed — never stored in plain text.
Username and password are NOT visible anywhere in the running app.

To change password:
    python3 -c "import hashlib; print(hashlib.sha256('YourNewPassword'.encode()).hexdigest())"
    Then replace the hash below.
"""

import hashlib
from typing import Tuple

# ── Single User Store ──────────────────────────────────────────
# DO NOT expose this dict in any UI element or log statement.

_USER: dict = {
    "username":      "Ali-datasmith",
    "display_name":  "Ali Datasmith",
    "role":          "admin",
    # sha256("Qx9#mK2$vL7@nR4!")
    "password_hash": "9cab649e5d1529a9413a51dab1e4bf50eb6b39d06cfd44874c89aeb28d613b98",
}

# ── Hash Utility ───────────────────────────────────────────────

def _hash(password: str) -> str:
    """Returns sha256 hex digest of a plain-text password."""
    return hashlib.sha256(password.encode()).hexdigest()

# ── Public API ─────────────────────────────────────────────────

def validate_credentials(username: str, password: str) -> Tuple[bool, str]:
    """
    Validates a username + password pair against the single user store.

    Args:
        username: Plain-text username from the login form
        password: Plain-text password from the login form

    Returns:
        (True,  welcome message) on success
        (False, generic error)   on failure — never reveals which field failed
    """
    if not username or not password:
        return False, "Username and password are required."

    username_match  = username.strip() == _USER["username"]
    password_match  = _hash(password)  == _USER["password_hash"]

    if username_match and password_match:
        return True, f"Welcome back, {_USER['display_name']}!"

    # Generic message — never reveal which field was wrong
    return False, "Invalid credentials. Access denied."


def get_display_name(username: str) -> str:
    """Returns display name for a valid username, else the username itself."""
    if username.strip() == _USER["username"]:
        return _USER["display_name"]
    return username


def get_role(username: str) -> str:
    """Returns role string for a valid username."""
    if username.strip() == _USER["username"]:
        return _USER["role"]
    return "viewer"
