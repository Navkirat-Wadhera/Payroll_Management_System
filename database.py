"""
database.py — Centralized DB connection and query functions.
All pages import from here. No raw SQL lives outside this file.
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def get_connection():
    """Return a fresh MySQL connection using .env credentials."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "payroll_db"),
    )


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

def verify_login(username: str, password: str) -> bool:
    """Return True if admin credentials match the Admins table."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT admin_id FROM Admins WHERE username = %s AND password = %s",
        (username, password),
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


# ---------------------------------------------------------------------------
# Departments
# ---------------------------------------------------------------------------

def get_departments() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Departments ORDER BY dept_id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_department(dept_id: int, dept_name: str, location: str) -> tuple[bool, str]:
    """Insert a new department. Returns (success, message)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Departments (dept_id, dept_name, location) VALUES (%s, %s, %s)",
            (dept_id, dept_name, location),
        )
        conn.commit()
        conn.close()
        return True, "Department added successfully."
    except mysql.connector.Error as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Employees
# ---------------------------------------------------------------------------

def get_employees() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT e.emp_id, e.emp_name, d.dept_name, e.base_salary, e.join_date
        FROM Employees e
        JOIN Departments d ON e.dept_id = d.dept_id
        ORDER BY e.emp_id
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_employee(emp_id: int, emp_name: str, dept_id: int, base_salary: float) -> tuple[bool, str]:
    """Insert a new employee. Returns (success, message)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Employees (emp_id, emp_name, dept_id, base_salary, join_date) VALUES (%s, %s, %s, %s, NOW())",
            (emp_id, emp_name, dept_id, base_salary),
        )
        conn.commit()
        conn.close()
        return True, "Employee added successfully."
    except mysql.connector.Error as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Attendance
# ---------------------------------------------------------------------------

def get_attendance() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT a.att_id, e.emp_name, a.att_date, a.status
        FROM Attendance a
        JOIN Employees e ON a.emp_id = e.emp_id
        ORDER BY a.att_date DESC
        LIMIT 200
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_attendance(emp_id: int, att_date: str, status: str) -> tuple[bool, str]:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Attendance (emp_id, att_date, status) VALUES (%s, %s, %s)",
            (emp_id, att_date, status),
        )
        conn.commit()
        conn.close()
        return True, "Attendance marked successfully."
    except mysql.connector.Error as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Payroll (Stored Procedure)
# ---------------------------------------------------------------------------

def run_payroll() -> tuple[bool, str, list[dict]]:
    """
    Call the credit_salary_batch() stored procedure.
    Returns (success, message, salary_records).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc("credit_salary_batch")
        # Consume any result sets produced by the procedure
        for _ in cursor.stored_results():
            pass
        conn.commit()

        # Fetch the newly inserted records
        cursor.execute(
            "SELECT * FROM Salary ORDER BY trans_id DESC"
        )
        records = cursor.fetchall()
        conn.close()
        return True, "Payroll processed successfully!", records
    except mysql.connector.Error as e:
        return False, str(e), []


def get_salary_records() -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Salary ORDER BY trans_id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------------------------------------------------------------------
# Dashboard Stats
# ---------------------------------------------------------------------------

def get_dashboard_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Employees")
    total_employees = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Departments")
    total_departments = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Salary")
    total_salary_records = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Attendance WHERE status = 'Absent'")
    total_absences = cursor.fetchone()[0]

    conn.close()
    return {
        "total_employees": total_employees,
        "total_departments": total_departments,
        "total_salary_records": total_salary_records,
        "total_absences": total_absences,
    }
