"""
pages/2_Departments.py — Add and view departments.
"""

import streamlit as st
from database import get_departments, add_department
import pandas as pd

# ── Auth guard ─────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(page_title="Departments | Payroll", page_icon="🏢", layout="wide")

# ── Header ─────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([6, 1])
with col_h1:
    st.title("🏢 Departments")
with col_h2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()

# ── Add Department Form ────────────────────────────────────────────────────
st.subheader("➕ Add New Department")

with st.form("add_dept_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    dept_id   = col1.number_input("Department ID", min_value=1, step=1)
    dept_name = col2.text_input("Department Name", placeholder="e.g. Finance")
    location  = col3.text_input("Location", placeholder="e.g. Mumbai")
    submitted = st.form_submit_button("Add Department", use_container_width=True)

if submitted:
    if not dept_name or not location:
        st.error("Please fill in all fields.")
    else:
        success, msg = add_department(int(dept_id), dept_name.strip(), location.strip())
        if success:
            st.success(f"✅ {msg}")
        else:
            st.error(f"❌ {msg}")

st.divider()

# ── Departments Table ──────────────────────────────────────────────────────
st.subheader("📋 All Departments")

depts = get_departments()
if depts:
    df = pd.DataFrame(depts)
    df.columns = ["Dept ID", "Department Name", "Location"]
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Total departments: **{len(depts)}**")
else:
    st.info("No departments found. Add one above.")
