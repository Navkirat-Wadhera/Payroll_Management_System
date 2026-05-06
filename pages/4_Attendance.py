"""
pages/4_Attendance.py — Mark and view employee attendance.
"""

import streamlit as st
from database import get_attendance, add_attendance, get_employees
import pandas as pd
from datetime import date

# ── Auth guard ─────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(page_title="Attendance | Payroll", page_icon="📅", layout="wide")

# ── Header ─────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([6, 1])
with col_h1:
    st.title("📅 Attendance")
with col_h2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()

# ── Mark Attendance Form ───────────────────────────────────────────────────
st.subheader("✏️ Mark Attendance")

employees = get_employees()
emp_options = {f"{e['emp_id']} — {e['emp_name']}": e["emp_id"] for e in employees}

if not emp_options:
    st.warning("⚠️ No employees found. Please add employees first.")
else:
    with st.form("mark_att_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        emp_label  = col1.selectbox("Employee", list(emp_options.keys()))
        att_date   = col2.date_input("Date", value=date.today())
        status     = col3.selectbox("Status", ["Present", "Absent"])
        submitted  = st.form_submit_button("Mark Attendance", use_container_width=True)

    if submitted:
        emp_id = emp_options[emp_label]
        success, msg = add_attendance(emp_id, str(att_date), status)
        if success:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")

st.divider()

# ── Attendance Table ───────────────────────────────────────────────────────
st.subheader("📋 Recent Attendance Records (Last 200)")

records = get_attendance()
if records:
    df = pd.DataFrame(records)
    df.columns = ["Att ID", "Employee Name", "Date", "Status"]

    # Colour-code status
    def highlight_status(val):
        if val == "Absent":
            return "background-color: #c0392b; color: white; font-weight: bold"
        return "background-color: #1e8449; color: white; font-weight: bold"

    styled = df.style.applymap(highlight_status, subset=["Status"])
    st.dataframe(styled, use_container_width=True, hide_index=True)
    st.caption(f"Showing latest **{len(records)}** records.")
else:
    st.info("No attendance records yet.")
