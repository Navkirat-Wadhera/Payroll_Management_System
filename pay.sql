-- 1. Create Database
CREATE DATABASE IF NOT EXISTS payroll_db;
USE payroll_db;

-- 2. Create Tables
CREATE TABLE Departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(50),
    location VARCHAR(50)
);

CREATE TABLE Employees (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    dept_id INT,
    base_salary DECIMAL(10, 2),
    join_date DATE,
    FOREIGN KEY (dept_id) REFERENCES Departments(dept_id)
);

CREATE TABLE Attendance (
    att_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT,
    att_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
);

CREATE TABLE Salary (
    trans_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT,
    month_year VARCHAR(20),
    base_salary DECIMAL(10,2),
    absences INT,
    deduction DECIMAL(10,2),
    net_salary DECIMAL(10, 2),
    processed_date DATE,
    FOREIGN KEY (emp_id) REFERENCES Employees(emp_id)
);

CREATE TABLE IF NOT EXISTS Admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50) 
);

-- 2. Create Default Admin User
-- Username: admin
-- Password: 123
INSERT INTO Admins (username, password) VALUES ('admin', '123');

-- 3. Stored Procedure (THE CORE LOGIC)
-- This procedure calculates deductions automatically based on Attendance table
DELIMITER //
CREATE PROCEDURE credit_salary_batch()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_emp_id INT;
    DECLARE v_base_salary DECIMAL(10,2);
    DECLARE v_absent_count INT;
    DECLARE v_deduction DECIMAL(10,2);
    DECLARE v_net DECIMAL(10,2);
    DECLARE v_hra DECIMAL(10,2);
    DECLARE v_tax DECIMAL(10,2);
    
    -- Cursor to fetch all employees
    DECLARE c_emp CURSOR FOR SELECT emp_id, base_salary FROM Employees;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN c_emp;

    read_loop: LOOP
        FETCH c_emp INTO v_emp_id, v_base_salary;
        IF done THEN
            LEAVE read_loop;
        END IF;

        -- 1. Count Absences for this employee
        SELECT COUNT(*) INTO v_absent_count 
        FROM Attendance 
        WHERE emp_id = v_emp_id AND status = 'Absent';

        -- 2. Calculate Deduction (1 Day Salary per absence)
        SET v_deduction = (v_base_salary / 30) * v_absent_count;

        -- 3. Calculate Allowances & Net
        SET v_hra = (v_base_salary - v_deduction) * 0.20;
        SET v_tax = (v_base_salary - v_deduction) * 0.05;
        SET v_net = (v_base_salary - v_deduction) + v_hra - v_tax;

        -- 4. Insert into Salary Table
        INSERT INTO Salary (emp_id, month_year, base_salary, absences, deduction, net_salary, processed_date)
        VALUES (v_emp_id, DATE_FORMAT(NOW(), '%M-%Y'), v_base_salary, v_absent_count, v_deduction, v_net, NOW());
        
    END LOOP;

    CLOSE c_emp;
END //
DELIMITER ;





