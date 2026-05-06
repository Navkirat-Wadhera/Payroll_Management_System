"""
seed_data.py — Populates the database with sample Indian employee data.
Run this AFTER setting up the database using pay.sql.

Usage:
    python seed_data.py
"""

import mysql.connector
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# --- DB CONFIG (loaded from .env) ---
db_config = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "payroll_db"),
}

# --- SAMPLE DATA (Indian Context) ---
first_names = [
    "Aarav", "Vihaan", "Aditya", "Rohan", "Arjun", "Sai", "Ishaan",
    "Krishna", "Vivaan", "Kabir", "Ananya", "Diya", "Saanvi", "Pari",
    "Myra", "Riya", "Aadhya", "Kiara", "Prisha", "Naira",
]
last_names = [
    "Sharma", "Patel", "Singh", "Kumar", "Gupta", "Reddy", "Verma",
    "Mehta", "Jain", "Chopra", "Yadav", "Mishra", "Das", "Rao",
    "Nair", "Iyer", "Gowda", "Khan", "Ali", "Malhotra",
]
dept_names = ["HR", "IT", "Sales", "Finance", "Marketing", "Operations", "Legal", "Logistics"]
locations  = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad"]
salaries   = [45000, 50000, 55000, 60000, 75000, 82000, 90000]


def get_connection():
    return mysql.connector.connect(**db_config)


def seed_database():
    conn   = get_connection()
    cursor = conn.cursor()

    # 0. Clean slate
    print("🧹 Clearing old data...")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in ("Salary", "Attendance", "Employees", "Departments"):
        cursor.execute(f"TRUNCATE TABLE {table}")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    print("   Tables wiped.")

    # 1. Departments
    print("🏢 Seeding Departments...")
    dept_ids = []
    for i, (name, loc) in enumerate(zip(dept_names, locations)):
        d_id = (i + 1) * 10
        dept_ids.append(d_id)
        cursor.execute(
            "INSERT INTO Departments (dept_id, dept_name, location) VALUES (%s, %s, %s)",
            (d_id, name, loc),
        )

    # 2. Employees (50 records)
    print("👥 Seeding Employees...")
    emp_ids = list(range(101, 151))
    for e_id in emp_ids:
        name   = f"{random.choice(first_names)} {random.choice(last_names)}"
        d_id   = random.choice(dept_ids)
        salary = random.choice(salaries)
        cursor.execute(
            "INSERT INTO Employees (emp_id, emp_name, dept_id, base_salary, join_date) VALUES (%s, %s, %s, %s, NOW())",
            (e_id, name, d_id, salary),
        )

    # 3. Attendance (400 records, ~20% absence rate)
    print("📅 Seeding Attendance...")
    statuses = ["Present", "Present", "Present", "Present", "Absent"]
    for _ in range(400):
        e_id = random.choice(emp_ids)
        att_date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
        status   = random.choice(statuses)
        try:
            cursor.execute(
                "INSERT INTO Attendance (emp_id, att_date, status) VALUES (%s, %s, %s)",
                (e_id, att_date, status),
            )
        except mysql.connector.Error:
            pass  # Skip duplicate entries

    conn.commit()
    conn.close()
    print("\n✅ Done! Seeded: 8 Departments | 50 Employees | ~400 Attendance records.")
    print("   You can now run:  streamlit run app.py")


if __name__ == "__main__":
    seed_database()