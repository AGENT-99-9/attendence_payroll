from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QPushButton, QDateEdit, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, QDate


class ViewEmployeesPage(QWidget):
    def __init__(self,stack):
        super().__init__()
        self.stack = stack
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2e7d32;
            }
            QPushButton {
                background-color: #2e7d32;
                color: white;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1b5e20;
            }
            QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
                padding: 4px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Heading
        heading = QLabel("View Employee Records")
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("font-size: 22px; color: #2e7d32;")
        main_layout.addWidget(heading)

        # Filter Layout
        filter_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name/contact...")
        filter_layout.addWidget(self.search_input)

        self.gender_filter = QComboBox()
        self.gender_filter.addItems(["All Genders", "Male", "Female", "Other"])
        filter_layout.addWidget(self.gender_filter)

        self.min_wage = QDoubleSpinBox()
        self.min_wage.setPrefix("Min ₹")
        self.min_wage.setRange(0, 99999.99)
        self.min_wage.setDecimals(2)
        filter_layout.addWidget(self.min_wage)

        self.max_wage = QDoubleSpinBox()
        self.max_wage.setPrefix("Max ₹")
        self.max_wage.setRange(0, 99999.99)
        self.max_wage.setDecimals(2)
        filter_layout.addWidget(self.max_wage)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("dd-MM-yyyy")
        self.start_date.setDate(QDate.currentDate().addMonths(-6))
        filter_layout.addWidget(self.start_date)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDisplayFormat("dd-MM-yyyy")
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date)

        main_layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Name", "Gender", "DOB", "Join Date", "Contact", "Daily Wage (₹)"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table)

        # Action buttons
        button_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.export_btn = QPushButton("Export to CSV")

        self.back_btn = QPushButton("Back")
        self.back_btn.setStyleSheet("background-color: green; color: white; font-weight: bold;")
        self.back_btn.clicked.connect(self.go_back)


        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.export_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def go_back(self):
        current_widget = self.stack.currentWidget()

        # Step 1: Remove it from the stack
        self.stack.removeWidget(current_widget)

        # Step 2: Delete it (optional but recommended)
        current_widget.deleteLater()
