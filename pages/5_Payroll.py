"""
pages/5_Payroll.py — Execute the MySQL stored procedure & view results.
"""

import streamlit as st
from database import run_payroll, get_salary_records
import pandas as pd

# ── Auth guard ─────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(page_title="Run Payroll | Payroll", page_icon="💰", layout="wide")

# ── Header ─────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([6, 1])
with col_h1:
    st.title("💰 Run Payroll")
with col_h2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()

# ── Explanation ────────────────────────────────────────────────────────────
st.info(
    """
    **How it works:**  
    Clicking **Execute Payroll** calls the MySQL Stored Procedure `credit_salary_batch()`.  
    The procedure loops through all employees using a **cursor**, counts absences from the  
    `Attendance` table, calculates deductions (1 day salary per absence), adds HRA (20%) and  
    deducts tax (5%), then inserts the final net salary into the `Salary` table.
    """,
    icon="ℹ️",
)

# ── Execute Payroll Button ─────────────────────────────────────────────────
st.subheader("⚙️ Execute Stored Procedure")

col_btn, col_spacer = st.columns([2, 5])
with col_btn:
    run_clicked = st.button("▶ Execute Payroll", type="primary", use_container_width=True)

if run_clicked:
    with st.spinner("Running `credit_salary_batch()` stored procedure…"):
        success, msg, records = run_payroll()
    if success:
        st.success(f"✅ {msg} — **{len(records)}** records processed.")
        st.session_state["payroll_records"] = records
    else:
        st.error(f"❌ {msg}")

st.divider()

# ── Salary Table ───────────────────────────────────────────────────────────
st.subheader("📋 Salary Records")

# Use newly processed records if available, else load from DB
records = st.session_state.get("payroll_records") or get_salary_records()

if records:
    df = pd.DataFrame(records)
    df.columns = ["Trans ID", "Emp ID", "Month", "Base Salary (₹)",
                  "Absences", "Deduction (₹)", "Net Salary (₹)", "Processed Date"]

    # Highlight net salary column
    def highlight_net(val):
        return "color: green; font-weight: bold"

    styled = df.style.applymap(highlight_net, subset=["Net Salary (₹)"])
    st.dataframe(styled, use_container_width=True, hide_index=True)
    st.caption(f"Total records: **{len(records)}**")
else:
    st.info("No salary records yet. Click **Execute Payroll** above to generate them.")
