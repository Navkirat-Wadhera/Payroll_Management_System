"""
app.py — Payroll Management System
Entry point: Login page.
Run with:  streamlit run app.py
"""

import streamlit as st
from database import verify_login

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Payroll Management System",
    page_icon="💼",
    layout="centered",
)

# ── If already logged in, redirect to dashboard ────────────────────────────
if st.session_state.get("logged_in"):
    st.switch_page("pages/1_Dashboard.py")

# ── UI ─────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; padding: 2rem 0 1rem 0;'>
        <h1 style='font-size:2.4rem;'>💼 Payroll Management System</h1>
        <p style='color:gray;'>Admin Portal — Please sign in to continue</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    with st.form("login_form"):
        st.subheader("🔐 Admin Login")
        username = st.text_input("Username", placeholder="admin")
        password = st.text_input("Password", type="password", placeholder="••••")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
        elif verify_login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Welcome, {username}! Redirecting…")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("❌ Invalid username or password.")

    st.caption("Default credentials → username: **admin** | password: **123**")