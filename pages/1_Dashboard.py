"""
pages/1_Dashboard.py — Overview stats for the Payroll System.
"""

import streamlit as st
from database import get_dashboard_stats, get_salary_records
import pandas as pd

# ── Auth guard ─────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(page_title="Dashboard | Payroll", page_icon="📊", layout="wide")

# ── Header ─────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([6, 1])
with col_h1:
    st.title("📊 Dashboard")
    st.caption(f"Logged in as **{st.session_state.get('username', 'Admin')}**")
with col_h2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()

# ── Stats cards ────────────────────────────────────────────────────────────
stats = get_dashboard_stats()

c1, c2, c3, c4 = st.columns(4)
c1.metric("👥 Total Employees",   stats["total_employees"])
c2.metric("🏢 Departments",       stats["total_departments"])
c3.metric("💰 Salary Records",   stats["total_salary_records"])
c4.metric("❌ Total Absences",   stats["total_absences"])

st.divider()

# ── Latest salary records ──────────────────────────────────────────────────
st.subheader("💵 Latest Salary Records")

records = get_salary_records()
if records:
    df = pd.DataFrame(records)
    df.columns = ["Trans ID", "Emp ID", "Month", "Base Salary (₹)",
                  "Absences", "Deduction (₹)", "Net Salary (₹)", "Processed Date"]
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No salary records yet. Go to **Run Payroll** to process salaries.")
