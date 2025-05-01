from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QStackedWidget, QMainWindow, QApplication
import sys
from backend import *  # Assuming you have the necessary database functions in your backend module.
from PyQt5.QtCore import Qt
from datetime import datetime
from PyQt5.QtWidgets import QComboBox,QMessageBox
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtCore import QTime


class AttendancePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #2e7d32;
                font-weight: bold;
                font-size: 24px;
                padding: 10px 0;
            }
            QPushButton {
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton#Submit {
                background-color: #2e7d32;
                color: white;
            }
            QPushButton#Back {
                background-color: #9e9e9e;
                color: white;
            }
            QPushButton#Save {
                background-color: #43a047;
                color: white;
            }
            QComboBox, QTimeEdit {
                border: 1px solid #cccccc;
                border-radius: 6px;
                padding: 4px;
            }
            QTableWidget {
                border: none;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #e8f5e9;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
        """)
        self.stack = stack
        self.manager = EmployeeManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        heading = QLabel("🕒 Mark Employee Attendance")
        layout.addWidget(heading)

        self.attendance_table = QTableWidget()
        self.attendance_table.setColumnCount(7)
        self.attendance_table.setHorizontalHeaderLabels([
            "Employee ID", "Employee Name", "Date", "In Time", "Out Time", "Status", "Remarks"
        ])
        self.attendance_table.verticalHeader().setVisible(False)
        layout.addWidget(self.attendance_table)

        # ✅ Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        submit_btn = QPushButton("Submit Attendance")
        submit_btn.setObjectName("Submit")
        submit_btn.clicked.connect(self.submit_attendance)

        save_btn = QPushButton("Save Attendance")
        save_btn.setObjectName("Save")
        save_btn.clicked.connect(self.save_attendance)

        modify_btn = QPushButton("Modify")
        modify_btn.setObjectName("Modify")
        modify_btn.clicked.connect(self.modify)

        back_btn = QPushButton("Back")
        back_btn.setObjectName("Back")
        back_btn.clicked.connect(self.go_back)

        for btn in (submit_btn, save_btn, back_btn,modify_btn):
            buttons_layout.addWidget(btn)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)
      
        

        

        # ✅ FIRST: set the number of rows
        self.initialize_empty_rows(len(self.initialize_attendance()))

        # ✅ THEN: populate the table
        self.populate_employee_data()

    def initialize_attendance(self):
        try:
            if self.manager.is_today_attendance_exist():
                self.employee_data = self.manager.get_today_attendance()
                print("this run")
            else:
                print("that run")
                self.employee_data = self.manager.get_all_employee_data()
            return self.employee_data
        except Exception as e:
            print(f"❌ Error while initializing attendance: {e}")
            return []




    

    def populate_employee_data(self):
        """Fetch employee data from the database and populate the attendance table."""
        from datetime import datetime
        from PyQt5.QtCore import Qt, QTime
        from PyQt5.QtWidgets import QTableWidgetItem, QTimeEdit, QComboBox

        self.employee_data = self.initialize_attendance()
        self.attendance_table.setRowCount(len(self.employee_data))

        print(self.employee_data)  # Debugging

        for i, employee in enumerate(self.employee_data):
            # Non-editable Employee ID
            id_item = QTableWidgetItem(str(employee['employee_id']))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.attendance_table.setItem(i, 0, id_item)

            print(employee['employee_id'])
            print(type(employee['employee_id']))

            # Fetch employee name from manager
            name = self.manager.get_employee_name_by_id(int(employee['employee_id']))
            print(name)

            # Non-editable Name
            name_item = QTableWidgetItem(name if name else "")
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.attendance_table.setItem(i, 1, name_item)

            # Non-editable Current Date
            current_date = datetime.now().strftime("%Y-%m-%d")
            date_item = QTableWidgetItem(current_date)
            date_item.setFlags(date_item.flags() & ~Qt.ItemIsEditable)
            self.attendance_table.setItem(i, 2, date_item)

            # In Time Picker
            in_time_picker = QTimeEdit()
            in_time_picker.setDisplayFormat("HH:mm")
            if "in_time" in employee and employee["in_time"]:
                # Convert to QTime if it's available
                in_time = QTime.fromString(employee["in_time"], "HH:mm")
                if in_time.isValid():
                    in_time_picker.setTime(in_time)
                else:
                    in_time_picker.setTime(QTime.currentTime())
            else:
                in_time_picker.setTime(QTime.currentTime())
            self.attendance_table.setCellWidget(i, 3, in_time_picker)

            # Out Time Picker
            out_time_picker = QTimeEdit()
            out_time_picker.setDisplayFormat("HH:mm")
            if "out_time" in employee and employee["out_time"]:
                out_time = QTime.fromString(employee["out_time"], "HH:mm")
                if out_time.isValid():
                    out_time_picker.setTime(out_time)
                else:
                    out_time_picker.setTime(QTime.currentTime())
            else:
                out_time_picker.setTime(QTime.currentTime())
            self.attendance_table.setCellWidget(i, 4, out_time_picker)

            # Status ComboBox
            status_combo = QComboBox()
            status_combo.addItems(["absent", "present", "leave"])
            if "status" in employee and employee["status"] in ["absent", "present", "leave"]:
                status_combo.setCurrentText(employee["status"])
            self.attendance_table.setCellWidget(i, 5, status_combo)

            # Editable Remarks
            remarks_text = employee.get("remarks", "") if isinstance(employee, dict) else ""
            remarks_item = QTableWidgetItem(remarks_text)
            self.attendance_table.setItem(i, 6, remarks_item)



    def initialize_empty_rows(self, num_rows):
        """Function to initialize empty rows for marking attendance"""
        self.attendance_table.setRowCount(num_rows)

    def submit_attendance(self):
        """Function to handle submitting attendance."""
        for row in range(self.attendance_table.rowCount()):
            # ✅ Safely get Employee ID
            emp_id_item = self.attendance_table.item(row, 0)
            emp_id = emp_id_item.text() if emp_id_item else ""

            # ✅ Safely get Name
            name_item = self.attendance_table.item(row, 1)
            name = name_item.text() if name_item else ""

            # ✅ Safely get Date
            date_item = self.attendance_table.item(row, 2)
            date = date_item.text() if date_item else ""

            # ✅ Safely get In Time
            in_time_widget = self.attendance_table.cellWidget(row, 3)
            in_time = in_time_widget.time().toString("HH:mm") if in_time_widget else ""

            # ✅ Safely get Out Time
            out_time_widget = self.attendance_table.cellWidget(row, 4)
            out_time = out_time_widget.time().toString("HH:mm") if out_time_widget else ""

            # ✅ Safely get Status
            status_widget = self.attendance_table.cellWidget(row, 5)
            status = status_widget.currentText().strip().lower() if status_widget else ""

            # ✅ Safely get Remarks
            remarks_item = self.attendance_table.item(row, 6)
            remarks = remarks_item.text().strip() if remarks_item else ""

            # ✅ Final Safety: Only submit if emp_id and date are present
            if emp_id and date:
                print(f"Employee ID: {emp_id}, Name: {name}, Date: {date}, In Time: {in_time}, Out Time: {out_time}, Status: {status}, Remarks: {remarks}")

                # ➡️ Save into database here (optional)
                self.manager.save_attendance(emp_id, date, in_time, out_time, status, remarks)
            else:
                print(f"⚠️ Skipping row {row+1}: Missing Employee ID or Date")

    def go_back(self):
            current_widget = self.stack.currentWidget()

            # Step 1: Remove it from the stack
            self.stack.removeWidget(current_widget)

            # Step 2: Delete it (optional but recommended)
            current_widget.deleteLater()

    def modify(self):
        """Save all attendance records to the database."""
        success_count = 0
        fail_count = 0

        for row in range(self.attendance_table.rowCount()):
            try:
                # Safely get data from the table
                emp_id_item = self.attendance_table.item(row, 0)
                emp_id = emp_id_item.text() if emp_id_item else ""
                
                date_item = self.attendance_table.item(row, 2)
                date = date_item.text() if date_item else ""

                in_time_widget = self.attendance_table.cellWidget(row, 3)
                in_time = in_time_widget.time().toString("HH:mm") if in_time_widget else ""

                out_time_widget = self.attendance_table.cellWidget(row, 4)
                out_time = out_time_widget.time().toString("HH:mm") if out_time_widget else ""

                status_widget = self.attendance_table.cellWidget(row, 5)
                status = status_widget.currentText().strip().lower() if status_widget else ""

                remarks_item = self.attendance_table.item(row, 6)
                remarks = remarks_item.text().strip() if remarks_item else ""

                # Validate the presence of emp_id and date
                if not emp_id or not date:
                    print(f"⚠️ Missing Employee ID or Date for row {row}, skipping...")
                    fail_count += 1
                    continue

                # Modify attendance in database
                self.manager.modify_attendance(emp_id, date, in_time, out_time, status, remarks)
                success_count += 1

            except Exception as e:
                print(f"❌ Failed to save attendance for row {row}: {e}")
                fail_count += 1

        # Show the result in a message box
        QMessageBox.information(self, "Save Attendance",
                                f"Attendance modified successfully!\n\nSuccess: {success_count}\nFailed: {fail_count}")

            
                
                

    
    def save_attendance(self):
        """Save all attendance records to the database and update is_submitted to 1."""
        success_count = 0
        fail_count = 0

        for row in range(self.attendance_table.rowCount()):
            try:
                # Safely get data from the table
                emp_id_item = self.attendance_table.item(row, 0)
                emp_id = emp_id_item.text() if emp_id_item else ""

                date_item = self.attendance_table.item(row, 2)
                date = date_item.text() if date_item else ""

                in_time_widget = self.attendance_table.cellWidget(row, 3)
                in_time = in_time_widget.time().toString("HH:mm") if in_time_widget else ""

                out_time_widget = self.attendance_table.cellWidget(row, 4)
                out_time = out_time_widget.time().toString("HH:mm") if out_time_widget else ""

                status_widget = self.attendance_table.cellWidget(row, 5)
                status = status_widget.currentText().strip().lower() if status_widget else ""

                remarks_item = self.attendance_table.item(row, 6)
                remarks = remarks_item.text().strip() if remarks_item else ""

                # Validate the presence of emp_id and date
                if not emp_id or not date:
                    print(f"⚠️ Missing Employee ID or Date for row {row}, skipping...")
                    fail_count += 1
                    continue

                # Save attendance record
                self.manager.save_attendance(emp_id, date, in_time, out_time, status, remarks)

                # Update is_submitted = 1 for this record
                self.manager.update_is_submitted(emp_id, date)

                success_count += 1

            except Exception as e:
                print(f"❌ Failed to save attendance for row {row}: {e}")
                fail_count += 1

        # Show the result in a message box
        QMessageBox.information(self, "Save Attendance",
                                f"Attendance saved successfully!\n\nSuccess: {success_count}\nFailed: {fail_count}")
