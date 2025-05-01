from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, QTableWidgetItem, QSizePolicy, QApplication, QPushButton
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys

class PayrollPage(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.setWindowTitle("Payroll Slip - Arogya Hospital")
        self.resize(794, 1123)  # Approx. A4 size in pixels (72dpi)
        self.setMinimumSize(794, 1123)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.init_ui()
        self.stack=stack


    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: 'Segoe UI';
                font-size: 13px;
            }
            QLabel {
                color: #333;
            }
            QFrame#line {
                border-top: 1px solid #ccc;
            }
        """)

        # Header: Logo + Hospital Info
        header_layout = QHBoxLayout()

        logo = QLabel()
        logo.setPixmap(QPixmap("hoslogo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo.setFixedWidth(120)

        hospital_info = QVBoxLayout()
        name_label = QLabel("AROGYA MULTISPECIALITY HOSPITAL")
        name_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        address_label = QLabel("123 Wellness Road, Sector 21, Delhi - 110021")
        contact_label = QLabel("Phone: +91-9876543210 | Email: contact@arogya.org")

        hospital_info.addWidget(name_label)
        hospital_info.addWidget(address_label)
        hospital_info.addWidget(contact_label)

        header_layout.addWidget(logo)
        header_layout.addLayout(hospital_info)
        layout.addLayout(header_layout)

        # Separator
        line = QFrame()
        line.setObjectName("line")
        layout.addWidget(line)

        # Employee Info Section
        layout.addSpacing(15)
        emp_info = QVBoxLayout()
        emp_info.addWidget(QLabel("Employee ID: EMP0987"))
        emp_info.addWidget(QLabel("Name: Dharampal Singh"))
        emp_info.addWidget(QLabel("Designation: Ward Boy"))
        emp_info.addWidget(QLabel("Department: Emergency Services"))
        emp_info.addWidget(QLabel("Salary Month: April 2025"))

        layout.addLayout(emp_info)

        # Spacer
        layout.addSpacing(20)

        # Salary Breakdown Table
        salary_table = QTableWidget(5, 2)
        salary_table.setHorizontalHeaderLabels(["Description", "Amount (₹)"])
        salary_table.verticalHeader().setVisible(False)
        salary_table.horizontalHeader().setStretchLastSection(True)
        salary_table.setEditTriggers(QTableWidget.NoEditTriggers)
        salary_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        salary_table.setFixedHeight(180)

        salary_table.setItem(0, 0, QTableWidgetItem("Basic Pay"))
        salary_table.setItem(0, 1, QTableWidgetItem("18,000"))

        salary_table.setItem(1, 0, QTableWidgetItem("HRA"))
        salary_table.setItem(1, 1, QTableWidgetItem("3,000"))

        salary_table.setItem(2, 0, QTableWidgetItem("Incentives"))
        salary_table.setItem(2, 1, QTableWidgetItem("2,000"))

        salary_table.setItem(3, 0, QTableWidgetItem("Deductions"))
        salary_table.setItem(3, 1, QTableWidgetItem("-1,500"))

        salary_table.setItem(4, 0, QTableWidgetItem("Net Pay"))
        salary_table.setItem(4, 1, QTableWidgetItem("21,500"))

        back_btn = QPushButton("Back")
        back_btn.setObjectName("Back")
        back_btn.clicked.connect(self.go_back)

        layout.addWidget(salary_table)
        layout.addWidget(back_btn)

        # Footer
        layout.addSpacing(40)
        footer = QLabel("This is a system-generated salary slip and does not require a signature.")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: gray; font-size: 11px;")
        layout.addWidget(footer)

        layout.addStretch()


    def go_back(self):
            current_widget = self.stack.currentWidget()

            # Step 1: Remove it from the stack
            self.stack.removeWidget(current_widget)

            # Step 2: Delete it (optional but recommended)
            current_widget.deleteLater()

