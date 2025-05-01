import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QMessageBox, QStackedWidget,QGroupBox,QComboBox, QDateEdit, QDoubleSpinBox,QFormLayout
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtCore import Qt,QTimer,QDateTime,QDate
import re

from backend import *
from attendace import *
from settings import *
from viewemp import *
from payroll import *

class MainDashboard(QMainWindow):
    def __init__(self,stack):
        super().__init__()
        self.stack = stack
        self.setWindowTitle("Dashboard")
        self.setMinimumSize(800, 600)
        self.init_ui()
        
       


    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)

        # Sidebar (Left)
        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background-color: #2D3B47; color: white; border-radius: 10px;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(15)

        # Admin Icon
        admin_icon = QLabel()
        admin_pixmap = QPixmap("admin_icon.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        admin_icon.setPixmap(admin_pixmap)
        admin_icon.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(admin_icon)

        # Welcome Label
        welcome_label = QLabel("Welcome Admin")
        welcome_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(welcome_label)

        # Date and Time
        self.datetime_label = QLabel()
        self.datetime_label.setFont(QFont("Segoe UI", 10))
        self.datetime_label.setAlignment(Qt.AlignCenter)
        self.update_time()

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)

        sidebar_layout.addWidget(self.datetime_label)

        # Navigation Buttons with Hover Effects
        buttons = ["Dashboard", "Reports", "Settings", "Logout"]
        for text in buttons:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(55, 65, 81, 0.7);  /* Semi-transparent dark slate */
                border: 1px solid #4b5563;                /* Subtle border */
                padding: 10px;
                border-radius: 8px;
                text-align: left;
                padding-left: 16px;
                font-size: 13px;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: rgba(59, 130, 246, 0.8); /* Soft blue hover */
                border: 1px solid #3b82f6;
            }
        """)

            btn.clicked.connect(self.on_button_click)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch(1)

        # Main Content (Right)
        content = QWidget()
        content_layout = QVBoxLayout(content)

        top_bar = QLabel("Dashboard")
        top_bar.setFont(QFont("Segoe UI", 20, QFont.Bold))
        top_bar.setStyleSheet("color: #111827;")
        top_bar.setAlignment(Qt.AlignLeft)
        
        # Create stacked widget for content display
        self.pages = QStackedWidget()
        self.pages.addWidget(self.create_dashboard_page())
        self.pages.addWidget(self.create_reports_page())
        self.pages.addWidget(self.create_settings_page())

        content_layout.addWidget(top_bar)
        content_layout.addWidget(self.pages)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

    def update_time(self):
        current = QDateTime.currentDateTime()
        self.datetime_label.setText(current.toString("dddd\n MMMM d, yyyy  \n hh:mm:ss AP"))

    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.soothing_colors = [
            "#fef2f2",  # Lighter Baby Pink (Cherry Blossom)
            "#e0e7ff",  # Pale Lavender Blue (Soft Sky)
            "#f0fdf4",  # Pale Mint Green (Fresh Dew)
            "#e0e7ff",  # Extra Soft Blue (Lavender Cloud)
            "#f0fdf4",  # Hint of Green (Mint Mist)
            "#fef2f2"   # Blush White (Soft Petal)
        ]



        # First HBox with 3 VBoxes
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.create_dashboard_pallet("Add Employee", self.add_employee, "C:/Users/Asus/Desktop/projects/arogya/1.png", self.soothing_colors[0]))
        hbox1.addWidget(self.create_dashboard_pallet("Attendance", self.view_attendance, "C:/Users/Asus/Desktop/projects/arogya/2.png", self.soothing_colors[1]))
        hbox1.addWidget(self.create_dashboard_pallet("Update Records", self.update_records, "C:/Users/Asus/Desktop/projects/arogya/3.png", self.soothing_colors[2]))

        # Second HBox with 3 VBoxes
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.create_dashboard_pallet("Generate Payroll", self.generate_payroll, "C:/Users/Asus/Desktop/projects/arogya/4.png", self.soothing_colors[3]))
        hbox2.addWidget(self.create_dashboard_pallet("View Records", self.view_records, "C:/Users/Asus/Desktop/projects/arogya/5.png", self.soothing_colors[4]))
        hbox2.addWidget(self.create_dashboard_pallet("Settings", self.settings, "C:/Users/Asus/Desktop/projects/arogya/6.png", self.soothing_colors[5]))

        # Add HBoxes to the grid layout
        grid_layout = QVBoxLayout()
        grid_layout.addLayout(hbox1)
        grid_layout.addLayout(hbox2)

        layout.addLayout(grid_layout)
        return page


    def create_dashboard_pallet(self, title, callback, image_path, color):
        pallet = QGroupBox(title)
        layout = QVBoxLayout()
        pallet.setLayout(layout)

        # Image section
        image_label = QLabel()
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setFixedSize(190, 170)# Adjust to taste

        # Pallet background and style
        stylesheet = f"""
            QGroupBox {{
                border: 2px solid gray;
                border-radius: 10px;
                background-color: {color};
            }}
        """
        pallet.setStyleSheet(stylesheet)

        # Button
        button = QPushButton(f"{title}")
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                background-color: #43a047;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        button.clicked.connect(callback)

        # Final layout
        layout.addWidget(image_label)
        layout.addWidget(button)
        layout.addStretch()

        pallet.setFixedSize(200, 200)
        return pallet


    def on_button_click(self):
        sender = self.sender()
        if sender.text() == "Dashboard":
            self.pages.setCurrentIndex(0)
        elif sender.text() == "Reports":
            self.pages.setCurrentIndex(1)
        elif sender.text() == "Settings":
            self.pages.setCurrentIndex(2)
        elif sender.text() == "Logout":
            self.stack.setCurrentIndex(0)

    # Placeholder functions for each functionality
    def add_employee(self):
        self.add_emp=AddEmployeePage(self.stack)
        self.stack.addWidget(self.add_emp)
        self.stack.setCurrentIndex(2)

    
    def view_attendance(self):
        self.add_attend=AttendancePage(self.stack)
        self.stack.addWidget(self.add_attend)
        self.stack.setCurrentIndex(2)

    def update_records(self):
        print("Updating Records...")

    def generate_payroll(self):
        
        self.payroll=PayrollPage(self.stack)
        self.stack.addWidget(self.payroll)
        self.stack.setCurrentIndex(2)
        self.payroll.resize(794, 1123)

    def view_records(self):
        self.view_emp=ViewEmployeesPage(self.stack)
        self.stack.addWidget(self.view_emp)
        self.stack.setCurrentIndex(2)

    def settings(self):
        self.settings_page=SettingsPage(self.stack)
        self.stack.addWidget(self.settings_page)
        self.stack.setCurrentIndex(2)

    def create_reports_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Reports Section"))
        layout.addWidget(QLabel("Add your report content here"))
        return page

    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Settings Section"))
        layout.addWidget(QLabel("Manage your settings here"))
        return page



class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.setGeometry(400, 200, 1000, 700)
        self.setMinimumSize(1000, 700)

        self.stack = QStackedWidget()
        self.initUI()
        self.setCentralWidget(self.stack)

    def initUI(self):
        # Create pages
        self.login_page = QWidget()
        self.dashboard = MainDashboard(self.stack)
        


        self.build_login_ui()

        # Add to stack
        self.stack.addWidget(self.login_page)   # index 0
        self.stack.addWidget(self.dashboard)    # index 1

        # Set initial page
        self.stack.setCurrentIndex(0)

    def build_login_ui(self):
        

        # Left image
        image_label = QLabel()
        pixmap = QPixmap("login_image.jpg")  # Replace with your own image
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right login form
        title = QLabel("Welcome Back 👋")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Please login to continue")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #f3f3f3;")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet(self.input_style())

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(self.input_style())

        login_btn = QPushButton("Login")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet(self.button_style())
        login_btn.clicked.connect(self.handle_login)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(30)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addSpacing(20)
        layout.addWidget(login_btn)
        layout.addStretch(2)

        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(40, 20, 40, 20)

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(image_label, 2)
        hbox.addWidget(frame, 1)

        self.login_page.setLayout(hbox)

    def input_style(self):
        return """
            QLineEdit {
                padding: 10px;
                border-radius: 15px;
                border: 2px solid white;
                background-color: rgba(255, 255, 255, 0.2);
                color: black;
            }
            QLineEdit:focus {
                border: 2px solid blue;
                background-color: rgba(255, 255, 255, 0.4);
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background-color: #ff758c;
                border: none;
                border-radius: 20px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: #ff6a88;
            }
        """

    def handle_login(self):
        username = self.username.text()
        password = self.password.text()
    
        if auth.authorize(username,password):
            QMessageBox.information(self, "Login Success", "Welcome Admin!")
            self.stack.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect credentials")



class AddEmployeePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f8;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }

            QLabel {
                color: #333;
            }

            QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 6px 8px;
                background-color: white;
            }

            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
                border: 1px solid #4CAF50;
                background-color: #fdfdfd;
            }

            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
                background-color: white;
            }

            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
                background-color: white;
                color: #4CAF50;
                font-weight: bold;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.init_ui()
        self.stack = stack
        self.emp_manager = EmployeeManager()  # Initialize EmployeeManager

    def init_ui(self):
        layout = QVBoxLayout()

        # Heading
        heading = QLabel("Add New Employee")
        heading.setStyleSheet("font-size: 24px; color: green; font-weight: bold;")
        heading.setFixedHeight(40)
        layout.addWidget(heading)

        # Form layout
        form_layout = QFormLayout()

        # Name
        self.name_input = QLineEdit()
        form_layout.addRow("Name:", self.name_input)

        # Gender
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Male", "Female", "Other"])
        form_layout.addRow("Gender:", self.gender_input)

        # Date of Birth
        self.dob_input = QDateEdit()
        self.dob_input.setCalendarPopup(True)
        self.dob_input.setMaximumDate(QDate.currentDate().addDays(-1))
        form_layout.addRow("Date of Birth:", self.dob_input)

        # Join Date (default: today)
        self.join_date_input = QDateEdit()
        self.join_date_input.setDate(QDate.currentDate())
        self.join_date_input.setCalendarPopup(True)
        form_layout.addRow("Join Date:", self.join_date_input)

        # Contact Number
        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("+91XXXXXXXXXX")
        form_layout.addRow("Contact Number:", self.contact_input)

        # Daily Wage (decimal)
        self.wage_input = QDoubleSpinBox()
        self.wage_input.setRange(0.01, 99999.99)
        self.wage_input.setDecimals(2)
        form_layout.addRow("Daily Wage (₹):", self.wage_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.back_btn.clicked.connect(self.go_back)

        

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.clear_btn.clicked.connect(self.clear_form)
        
        self.submit_btn = QPushButton("Submit")
        self.submit_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.submit_btn.clicked.connect(self.submit_form)

        button_layout.addWidget(self.back_btn)
        
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.submit_btn)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def go_back(self):
        current_widget = self.stack.currentWidget()

        # Step 1: Remove it from the stack
        self.stack.removeWidget(current_widget)

        # Step 2: Delete it (optional but recommended)
        current_widget.deleteLater()

    def clear_form(self):
        self.name_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.dob_input.setDate(QDate.currentDate())
        self.join_date_input.setDate(QDate.currentDate())
        self.contact_input.clear()
        self.wage_input.setValue(0.00)

    def submit_form(self):
        name = self.name_input.text().strip()
        gender = self.gender_input.currentText()
        dob = self.dob_input.date().toString("yyyy-MM-dd")
        join_date = self.join_date_input.date().toString("yyyy-MM-dd")
        contact = self.contact_input.text().strip()
        daily_wage = self.wage_input.value()

        # Input validation
        if not name:
            QMessageBox.warning(self, "Error", "Please enter employee name.")
            return
        if gender == "Select Gender":
            QMessageBox.warning(self, "Error", "Please select a gender.")
            return
        if not re.fullmatch(r"\+91\d{10}", contact):
            QMessageBox.warning(self, "Error", "Enter valid contact: +91 followed by 10 digits.")
            return
        if daily_wage <= 0:
            QMessageBox.warning(self, "Error", "Daily wage must be a positive value.")
            return

        # Pass data to EmployeeManager to add employee
        success = self.emp_manager.add_employee(name, gender, dob, join_date, contact, daily_wage)

        if success:
            # Show success message
            QMessageBox.information(self, "Success", "Employee added successfully!")

            # Clear form after submission
            self.clear_form()
        else:
            QMessageBox.warning(self, "Error", "Failed to add employee. Please try again.")


if __name__ == "__main__":
    setup_initializer()
    auth=Auth()
    app = QApplication(sys.argv)
    window = AdminApp()
    window.show()
    sys.exit(app.exec_())
