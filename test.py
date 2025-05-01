from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QComboBox, QDoubleSpinBox, QPushButton, QGridLayout, QTextEdit, QMessageBox,
    QFrame
)
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QLinearGradient, QBrush

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame,
    QSizePolicy, QMessageBox, QStackedWidget,QGroupBox,QComboBox, QDateEdit, QDoubleSpinBox,QFormLayout
)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor, QLinearGradient, QBrush
from PyQt5.QtCore import Qt,QTimer,QDateTime,QDate
import re
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem



class SalarySlipUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Salary Slip")
        self.setGeometry(100, 100, 1000, 800)
        self.initUI()
        self.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
            background-color: #f7fafd;
        }
        QLabel {
            color: #333;
        }
        QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit {
            padding: 0px;
            border: 1px solid #ccc;
            border-radius: 6px;
            background-color: #fff;
        }
        QComboBox {
            min-width: 150px;
        }
        QPushButton {
            background-color: #0078d7;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #005ea6;
        }
        QTableWidget {
            background-color: white;
            border: 1px solid #ccc;
            border-radius: 6px;
        }
        QTableWidget::item {
            padding: 6px;
        }
    """)


    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Salary Slip")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")
        title.setStyleSheet("""
        font-size: 32px; 
        font-weight: bold; 
        color: #005ea6;
        margin-bottom: 20px;
    """)

        layout.addWidget(title)

        # Company Info
        layout.addWidget(self.sectionLabel("Company Information"))
        h1layout=QHBoxLayout()
       
       
        
       

        self.hospital_name = QLabel("Arogya Multispeciality Hospital")
        self.address = QLabel("SAI NAGAR, NTPC ROAD, Unchahar, Uttar Pradesh 229406")
        self.phone = QLabel("+91 9988881121")
        self.email = QLabel("arogya@gmail.com")
        self.timing = QLabel("Open for 24 Hrs")
        v1layout = QFormLayout()
        v1layout.setLabelAlignment(Qt.AlignLeft)
        v1layout.setFormAlignment(Qt.AlignLeft)

        v1layout.addRow("Hospital Name:", self.hospital_name)
        v1layout.addRow("Address:", self.address)
        v1layout.addRow("Phone:", self.phone)
        v1layout.addRow("Email:", self.email)
        v1layout.addRow("Timings:", self.timing)


        logo_label = QLabel()
        pixmap = QPixmap("hoslogo.png")  # Provide the correct path
        pixmap = QPixmap("hoslogo.png")
        if pixmap.isNull():
            logo_label.setText("Logo not found")
        else:
            pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)


        h1layout.addLayout(v1layout)
        h1layout.addWidget(logo_label,alignment=Qt.AlignRight)

        layout.addLayout(h1layout)

        # Employee Info
        layout.addWidget(self.sectionLabel("Employee Information"))
        self.emp_id = QComboBox()
        self.emp_id.addItems(["Select", "E001", "E002", "E003"])
        self.emp_id.currentIndexChanged.connect(self.fillEmployeeDetails)
        self.emp_name = QLabel()
        self.gender = QLabel()
        self.emp_phone = QLabel()

        layout.addLayout(self.formRow("Employee ID:", self.emp_id))
        layout.addLayout(self.formRow("Name:", self.emp_name))
        layout.addLayout(self.formRow("Gender:", self.gender))
        layout.addLayout(self.formRow("Phone:", self.emp_phone))

        # Earnings and Deductions Table
        layout.addWidget(self.sectionLabel("Earnings and Deductions"))

        self.earnings = {}
        self.deductions = {}

        earnings_list = ["Basic", "Bonus", "Over Time Pay"]
        deductions_list = ["Salary Advance", "Other Deduction"]
        max_rows = max(len(earnings_list), len(deductions_list))

        self.table = QTableWidget(max_rows, 4)
        self.table.setHorizontalHeaderLabels(["Earnings", "Amount", "Deductions", "Amount"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        for i in range(max_rows):
            # Earnings side
            if i < len(earnings_list):
                self.table.setItem(i, 0, QTableWidgetItem(earnings_list[i]))
                spin = QDoubleSpinBox()
                spin.setPrefix("Rs ")
                spin.setMaximum(999999.99)
                spin.valueChanged.connect(self.updateNetPay)
                self.table.setCellWidget(i, 1, spin)
                self.earnings[earnings_list[i]] = spin

            # Deductions side
            if i < len(deductions_list):
                self.table.setItem(i, 2, QTableWidgetItem(deductions_list[i]))
                spin = QDoubleSpinBox()
                spin.setPrefix("Rs ")
                spin.setMaximum(999999.99)
                spin.valueChanged.connect(self.updateNetPay)
                self.table.setCellWidget(i, 3, spin)
                self.deductions[deductions_list[i]] = spin

        layout.addWidget(self.table)

        # Net Pay
        self.net_pay = QLabel()
        self.in_words = QLabel()
        self.in_words.setFixedHeight(40)
       
       

        layout.addLayout(self.formRow("Net Pay:", self.net_pay))
        layout.addLayout(self.formRow("In Words:", self.in_words))

        # Signatures
        prepared_by = QLineEdit()
        received_by = QLineEdit()
        form1 = self.formRow("Prepared By:", prepared_by)
        form2 = self.formRow("Received By:", received_by)

        h2layout = QHBoxLayout()
        h2layout.addLayout(form1)
        h2layout.addLayout(form2)
        layout.addLayout(h2layout)

        

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Back"))
        btn_layout.addWidget(QPushButton("Preview"))
        btn_layout.addWidget(QPushButton("Generate"))
        btn_layout.addWidget(QPushButton("Export as PDF"))
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def sectionLabel(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; font-size: 16px; background-color: #D0E6FF; padding: 4px;")
        return label

    def formRow(self, label_text, widget):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFixedWidth(120)  # You can adjust this width
        layout.addWidget(label)
        layout.addWidget(widget)
        layout.setSpacing(10)  # Optional: reduce gap between label and widget
        return layout


    def fillEmployeeDetails(self):
        data = {
            "E001": ("Dharampal", "Male", "9999999999"),
            "E002": ("Dayaraam", "Male", "8888888888"),
            "E003": ("Savita", "Female", "7777777777"),
        }
        selected = self.emp_id.currentText()
        if selected in data:
            name, gender, phone = data[selected]
            self.emp_name.setText(name)
            self.gender.setText(gender)
            self.emp_phone.setText(phone)
        else:
            self.emp_name.clear()
            self.gender.clear()
            self.emp_phone.clear()

    def updateNetPay(self):
        total_earnings = sum(spin.value() for spin in self.earnings.values())
        total_deductions = sum(spin.value() for spin in self.deductions.values())
        net = total_earnings - total_deductions
        self.net_pay.setText(f"Rs {net:.2f}")
        self.in_words.setText(self.convertToWords(net))

    def convertToWords(self, amount):
        # Very basic converter for demonstration
        return f"Rupees {amount:,.2f} only"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SalarySlipUI()
    window.show()
    sys.exit(app.exec_())
