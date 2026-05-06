"""
pages/3_Employees.py — Add and view employees.
"""

import streamlit as st
from database import get_employees, add_employee, get_departments
import pandas as pd

# ── Auth guard ─────────────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    st.switch_page("app.py")

st.set_page_config(page_title="Employees | Payroll", page_icon="👥", layout="wide")

# ── Header ─────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([6, 1])
with col_h1:
    st.title("👥 Employees")
with col_h2:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.divider()

# ── Add Employee Form ──────────────────────────────────────────────────────
st.subheader("➕ Add New Employee")

# Fetch departments for dropdown
depts = get_departments()
dept_options = {f"{d['dept_id']} — {d['dept_name']}": d["dept_id"] for d in depts}

if not dept_options:
    st.warning("⚠️ No departments found. Please add a department first.")
else:
    with st.form("add_emp_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        emp_id      = col1.number_input("Employee ID", min_value=1, step=1)
        emp_name    = col2.text_input("Full Name", placeholder="e.g. Aarav Sharma")

        col3, col4 = st.columns(2)
        dept_label  = col3.selectbox("Department", list(dept_options.keys()))
        base_salary = col4.number_input("Base Salary (₹)", min_value=0.0, step=1000.0)

        submitted = st.form_submit_button("Add Employee", use_container_width=True)

    if submitted:
        if not emp_name:
            st.error("Please enter the employee name.")
        else:
            dept_id = dept_options[dept_label]
            success, msg = add_employee(int(emp_id), emp_name.strip(), dept_id, base_salary)
            if success:
                st.success(f"✅ {msg}")
            else:
                st.error(f"❌ {msg}")

st.divider()

# ── Employees Table ────────────────────────────────────────────────────────
st.subheader("📋 All Employees")

employees = get_employees()
if employees:
    df = pd.DataFrame(employees)
    df.columns = ["Emp ID", "Name", "Department", "Base Salary (₹)", "Join Date"]
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.caption(f"Total employees: **{len(employees)}**")
else:
    st.info("No employees found. Add one above.")
