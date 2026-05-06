# Payroll Management System

A **Python + Streamlit + MySQL** web application for managing employee payroll. Built as a Database Management Systems (DBMS) project demonstrating core database concepts including stored procedures, foreign key constraints, cursors, and relational schema design.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🔐 Admin Login | Secure login validated against the `Admins` MySQL table |
| 🏢 Department Management | Add and view company departments |
| 👥 Employee Management | Add employees linked to departments via foreign key |
| 📅 Attendance Tracking | Mark daily attendance (Present / Absent) per employee |
| 💰 Payroll Processing | Execute a MySQL **Stored Procedure** to auto-calculate net salary |
| 📊 Dashboard | Live stats — total employees, departments, salary records, absences |

---

## 🗄️ Database Concepts Used

- **Relational Schema** — 5 normalized tables with foreign key relationships
- **Stored Procedure** — `credit_salary_batch()` uses a **cursor** to loop all employees and calculate deductions
- **Salary Formula:**
  - Deduction = (Base Salary ÷ 30) × Absences
  - HRA = 20% of (Base − Deduction)
  - Tax = 5% of (Base − Deduction)
  - **Net Salary = (Base − Deduction) + HRA − Tax**
- **Joins** — Attendance and Employee tables joined for readable reports

---

## 🗂️ Project Structure

```
payroll-management-system/
│
├── app.py              # Streamlit entry point (Login page)
├── database.py         # All DB connection + query functions
├── seed_data.py        # Seed script — populates DB with sample data
├── pay.sql             # Full MySQL schema + stored procedure
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Departments.py
│   ├── 3_Employees.py
│   ├── 4_Attendance.py
│   └── 5_Payroll.py
│
├── .env.example        # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- MySQL Server (XAMPP / MySQL Workbench / any MySQL installation)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/Navkirat-Wadhera/Payroll_Management_System.git
cd payroll-management-system
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Configure Database Credentials
```bash
# Copy the example file
cp .env.example .env

# Edit .env and set your MySQL password
```

`.env` file:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=payroll_db
```

### Step 4 — Set Up the Database
Open **MySQL Workbench** (or any MySQL client) and run:
```sql
SOURCE pay.sql;
```
This creates the database, all tables, the admin user, and the stored procedure.

### Step 5 — (Optional) Seed Sample Data
```bash
python seed_data.py
```
This populates the database with **8 departments**, **50 employees**, and **~400 attendance records**.

### Step 6 — Run the Application
```bash
streamlit run app.py
```
Open your browser at **http://localhost:8501**

**Default Login:**
- Username: `admin`
- Password: `123`

---

## 🗃️ Database Schema

```
Departments          Employees
───────────          ─────────
dept_id (PK)  ◄──── dept_id (FK)
dept_name            emp_id (PK)
location             emp_name
                     base_salary
                     join_date
                        │
              ┌─────────┘
              ▼
Attendance              Salary
──────────              ──────
att_id (PK)             trans_id (PK)
emp_id (FK)  ◄────────  emp_id (FK)
att_date                month_year
status                  base_salary
                        absences
                        deduction
                        net_salary
                        processed_date

Admins
──────
admin_id (PK)
username (UNIQUE)
password
```

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=flat&logo=pandas&logoColor=white)

---

## 👤 Author

**Navkirat Singh Wadhera**

> Built as a Database Management Systems (DBMS) project showcasing MySQL stored procedures, relational schema design, and Python-based full-stack development.
