import sqlite3
import os
from datetime import datetime

from datetime import date

def setup_initializer():
    # Connect to SQLite database
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()

    # Check if setup has already been completed by looking for a setup flag in the database
    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='setup_flag'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS setup_flag (
            flag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            setup_done BOOLEAN NOT NULL
        )
        """)

        # Insert setup completion flag if the setup table is empty
        cursor.execute("SELECT COUNT(*) FROM setup_flag")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO setup_flag (setup_done) VALUES (1)")  # 1 means setup is done
            print("Setup completed successfully.")

            # Proceed with creating all necessary tables and inserting default data
            create_tables_and_default_data(cursor)
            

            conn.commit()
        else:
            print("Setup has already been completed....")
    else:
        print("Setup has already been completed.")

    # Close connection
    conn.close()



from datetime import datetime

def create_tables_and_default_data(cursor):
    # Create employee table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gender TEXT NOT NULL,
        dob DATE NOT NULL,
        joining_date DATE NOT NULL,
        contact_number TEXT NOT NULL,
        daily_wage REAL NOT NULL CHECK(daily_wage >= 0),
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create attendance table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'leave')),
        remarks TEXT,
        in_time TEXT,
        out_time TEXT,
        is_submitted BOOLEAN DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(employee_id) REFERENCES employee(id)
        UNIQUE (employee_id, date)
    );
    """)

    # Create payroll table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        employee_id INTEGER NOT NULL,
        employee_name TEXT NOT NULL,

        month TEXT NOT NULL,                            -- Format: YYYY-MM
        total_present_days INTEGER NOT NULL CHECK(total_present_days >= 0),
        total_working_days INTEGER NOT NULL CHECK(total_working_days > 0),

        daily_wage REAL NOT NULL CHECK(daily_wage >= 0),

        basic_salary REAL GENERATED ALWAYS AS (daily_wage * total_present_days) STORED,

        deductions REAL DEFAULT 0 CHECK(deductions >= 0),
        bonus REAL DEFAULT 0 CHECK(bonus >= 0),

        net_salary REAL GENERATED ALWAYS AS (basic_salary + bonus - deductions) STORED,

        amount_paid REAL DEFAULT 0 CHECK(amount_paid >= 0),

        generated_on TEXT NOT NULL,                     -- Format: YYYY-MM-DD
        status TEXT NOT NULL CHECK(status IN ('Paid', 'Not Paid')),

        FOREIGN KEY (employee_id) REFERENCES employee(id)
    );

    """)

    # Create auth table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auth (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    );
    """)

    # Insert a default auth user
    cursor.execute("""
    INSERT INTO auth (username, password) VALUES (?, ?)
    """, ('a', 'a'))

    print("hogaya")  # success message

    # Insert default data for employee
    default_employee_data = [
        ("John Doe", "Male", "1980-01-01", "2020-06-15", "1234567890", 500.0),
        ("Jane Smith", "Female", "1990-05-12", "2021-09-01", "0987654321", 600.0)
    ]
    cursor.executemany("""
    INSERT INTO employee (name, gender, dob, joining_date, contact_number, daily_wage)
    VALUES (?, ?, ?, ?, ?, ?)
    """, default_employee_data)

    # Insert default data for attendance
    default_attendance_data = [
        (1, "2025-04-22", "present", "N/A", "09:00 AM", "05:00 PM", 1),
        (2, "2025-04-22", "absent", "N/A", None, None, 0)
    ]
    cursor.executemany("""
    INSERT INTO attendance (employee_id, date, status, remarks, in_time, out_time, is_submitted)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, default_attendance_data)

    # Insert default data for payroll
   # Default payroll data (Updated to include new fields: employee_name, total_working_days, daily_wage)
    default_payroll_data = [
        (1, "John Doe", "2025-04", 20, 30, 500.0, 0.0, 0.0, datetime.now().strftime('%Y-%m-%d'), "Not Paid"),
        (2, "Jane Smith", "2025-04", 22, 30, 600.0, 0.0, 0.0, datetime.now().strftime('%Y-%m-%d'), "Not Paid")
    ]

    # Execute the insert query with the new structure
    cursor.executemany("""
    INSERT INTO payroll (employee_id, employee_name, month, total_present_days, total_working_days, daily_wage, deductions, bonus, generated_on, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, default_payroll_data)




import sqlite3

class Auth:
    def __init__(self, db_path='company.db'):
        self.db_path = db_path

    def _connect(self):
        """ Helper method to connect to the database. """
        return sqlite3.connect(self.db_path)


    def setup_admin(self, username, password):
        """ Set up the admin credentials if not already set. """
     

        # Check if admin already exists
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auth WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            print("Admin already exists.")
        else:
            # Insert the new admin credentials into the database
            cursor.execute("INSERT INTO auth (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            print(f"Admin created with username: {username}")
        
        conn.close()

    def authorize(self, username, password):
        """ Verify the admin credentials. """
        

        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM auth WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()

        if result:
            print("Authorization successful.")
            return True
        else:
            print("Invalid username or password.")
            return False

    def change_admin(self, old_username, old_password, new_username, new_password):
        """ Reset the admin's username and password. """
        self._create_auth_table()

        conn = self._connect()
        cursor = conn.cursor()

        # Verify the old admin credentials
        cursor.execute("SELECT * FROM auth WHERE username = ? AND password = ?", (old_username, old_password))
        result = cursor.fetchone()

        if result:
            # Update with new username and password
            cursor.execute("UPDATE auth SET username = ?, password = ? WHERE username = ?",
                           (new_username, new_password, old_username))
            conn.commit()
            print(f"Admin credentials updated. New username: {new_username}")
        else:
            print("Old username or password is incorrect.")

        conn.close()




class EmployeeManager:
    def __init__(self, db_path='company.db'):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)
    def add_employee(self, name, gender, dob, joining_date, contact_number, daily_wage):
        """Add a new employee to the employee table."""
        conn = self._connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO employee (name, gender, dob, joining_date, contact_number, daily_wage)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, gender, dob, joining_date, contact_number, daily_wage))
            
            conn.commit()
            print(f"Employee '{name}' added successfully.")
        except sqlite3.Error as e:
            print(f"Failed to add employee. Error: {e}")
        finally:
            conn.close()


  

    def add_payroll(self, employee_id, month, total_present_days, total_salary, amount_paid, generated_on, status):
        """Add a payroll record for an employee."""
        conn = self._connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO payroll (employee_id, month, total_present_days, total_salary, amount_paid, generated_on, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (employee_id, month, total_present_days, total_salary, amount_paid, generated_on, status))
            
            conn.commit()
            print(f"Payroll for employee ID {employee_id} for the month of {month} added successfully.")
        except sqlite3.Error as e:
            print(f"Failed to add payroll. Error: {e}")
        finally:
            conn.close()

    
    def get_all_employee_data(self):
        """Fetch all employee data from the database and return it in a proper format."""
        conn = self._connect()
        cursor = conn.cursor()

        # Correct SQL query based on your table definition
        query = "SELECT id, name, dob, gender, contact_number, daily_wage, joining_date FROM employee"

        try:
            cursor.execute(query)
            rows = cursor.fetchall()

            # Properly include all the fetched fields
            employee_data = []
            for row in rows:
                employee = {
                    'employee_id': row[0],
                    'name': row[1],
                    'dob': row[2],
                    'gender': row[3],
                    'contact': row[4],
                    'daily_wage': row[5],
                    'join_date': row[6]
                }
                employee_data.append(employee)

            return employee_data

        except sqlite3.Error as e:
            print(f"Error fetching employee data: {e}")
            return []

        finally:
            conn.close()


    def save_attendance(self, employee_id, date, in_time, out_time, status, remarks):
        """Save or update attendance record in the database for a given employee."""
        conn = self._connect()
        cursor = conn.cursor()
        try:
            # Enable faster commit after multiple operations
            conn.execute("BEGIN")

            # Insert or Update automatically if record already exists
            cursor.execute("""
                INSERT INTO attendance (employee_id, date, in_time, out_time, status, remarks, is_submitted)
                VALUES (?, ?, ?, ?, ?, ?, 1)
                ON CONFLICT(employee_id, date)
                DO UPDATE SET 
                    in_time = excluded.in_time,
                    out_time = excluded.out_time,
                    status = excluded.status,
                    remarks = excluded.remarks,
                    is_submitted = 1
            """, (
                employee_id,
                date,
                in_time if in_time else None,
                out_time if out_time else None,
                status.strip().lower() if status else None,
                remarks.strip() if remarks else None
            ))

            conn.commit()
            print(f"✅ Attendance saved/updated for Employee ID: {employee_id} on {date}")

        except Exception as e:
            conn.rollback()
            print(f"❌ Error saving attendance for Employee ID {employee_id} on {date}: {e}")

        finally:
            conn.close()


    def modify_attendance(self, employee_id, date, in_time, out_time, status, remarks):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            # Check if the record exists
            cursor.execute("""
                SELECT 1 FROM attendance
                WHERE employee_id = ? AND date = ?
            """, (employee_id, date))
            
            if cursor.fetchone():
                # Update the record
                cursor.execute("""
                    UPDATE attendance
                    SET in_time = ?, out_time = ?, status = ?, remarks = ?
                    WHERE employee_id = ? AND date = ?
                """, (
                    in_time if in_time else None,
                    out_time if out_time else None,
                    status.strip().lower() if status else None,
                    remarks.strip() if remarks else None,
                    employee_id,
                    date
                ))
                conn.commit()
                print(f"✅ Attendance modified for Employee ID: {employee_id} on {date}")
            else:
                print(f"⚠️ No existing attendance found for Employee ID: {employee_id} on {date}, cannot modify.")

        except Exception as e:
            print(f"❌ Error modifying attendance for Employee ID {employee_id} on {date}: {e}")
        finally:
            conn.close()

    def get_today_attendance(self):
        from datetime import datetime  # Make sure you have imported this at the top
        
        today = datetime.now().strftime("%Y-%m-%d")
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT employee_id, date, in_time, out_time, status, remarks
                FROM attendance
                WHERE date = ?
            """, (today,))
            rows = cursor.fetchall()

            attendance_list = []
            for row in rows:
                attendance_list.append({
                    "employee_id": row[0],
                    "date": row[1],
                    "in_time": row[2],
                    "out_time": row[3],
                    "status": row[4],
                    "remarks": row[5]
                })
            
            if not attendance_list:
                print("ℹ️ No attendance records found for today.")

            return attendance_list

        except Exception as e:
            print(f"❌ Error while fetching today's attendance: {e}")
            return []

        finally:
            conn.close()




    def is_today_attendance_exist(self):
        conn = self._connect()
        cursor = conn.cursor()
        today = date.today().strftime('%Y-%m-%d')

        try:
            cursor.execute("""
                SELECT COUNT(*) FROM attendance WHERE date = ?
            """, (today,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"❌ Error while checking today's attendance: {e}")
            return False
        finally:
            conn.close()

    def reset_database(self):
        try:
            # Connect to the database
            conn = self._connect()  # Assuming _connect() is a method that returns the connection
            cursor = conn.cursor()

            # Execute delete operations
            cursor.execute("DELETE FROM employee")
            cursor.execute("DELETE FROM attendance")
            cursor.execute("DELETE FROM payroll")
            cursor.execute("DELETE FROM setup_flag")
            cursor.execute("DELETE FROM auth")


            # Commit the changes to the database
            conn.commit()

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except Exception as e:
            # If an error occurs, roll back the changes
            if conn:
                conn.rollback()
            
            # Close the connection and cursor if they were opened
            if cursor:
                cursor.close()
            if conn:
                conn.close()

            # Raise the error for further handling in the UI or logs
            raise Exception(f"❌ Failed to reset database: {str(e)}")
    
    def get_employee_name_by_id(self, emp_id):
        """Fetch employee name based on their ID."""
        conn = self._connect()  # Open connection
        cursor = conn.cursor()
        try:
            query = "SELECT name FROM employee WHERE id = ?"
            cursor.execute(query, (emp_id,))
            result = cursor.fetchone()   # <-- you wrote self.cursor.fetchone() by mistake
            
            if result:
                return result[0]  # Return the name
            else:
                return None  # No employee found

        except Exception as e:
            print(f"Error fetching employee name: {e}")
            return None

        finally:
            conn.close()  # Always close the connection

    def update_is_submitted(self, emp_id, date):
        """Update is_submitted = 1 for the given employee and date."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            query = "UPDATE attendance SET is_submitted = 1 WHERE employee_id = ? AND date = ?"
            cursor.execute(query, (emp_id, date))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Failed to update is_submitted: {e}")
