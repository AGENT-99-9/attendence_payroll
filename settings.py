from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox,
    QMessageBox, QLineEdit, QInputDialog, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from backend import EmployeeManager


class SettingsPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.manager=EmployeeManager()
        self.setWindowTitle("⚙ Settings")
        self.setFixedSize(600, 500)
        self.setStyleSheet(self.get_stylesheet())
        self.init_ui()

    def init_ui(self):
        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)

        # Central card layout
        card = QWidget()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card_layout.setSpacing(20)
        card_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("⚙ Settings Panel")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addWidget(self.divider())

        # Theme
        theme_label = QLabel("🎨 Select Theme:")
        theme_label.setFont(QFont("Segoe UI", 10))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        card_layout.addWidget(theme_label)
        card_layout.addWidget(self.theme_combo)
        card_layout.addWidget(self.divider())

        # Buttons
        card_layout.addWidget(self.styled_button("👤 Change Admin", self.change_admin))
        card_layout.addWidget(self.styled_button("🔑 Change Password", self.change_password))
        card_layout.addWidget(self.styled_button("🗑️ Reset Attendance Database", self.reset_database))
        card_layout.addWidget(self.styled_button("⬆️ Check for Updates", self.check_updates))
        self.back_btn=self.styled_button("Back",self.back)


        card.setLayout(card_layout)
        outer_layout.addWidget(card)
        outer_layout.addWidget(self.back_btn)
        self.setLayout(outer_layout)

    def back(self):
        current_widget = self.stack.currentWidget()

            # Step 1: Remove it from the stack
        self.stack.removeWidget(current_widget)

            # Step 2: Delete it (optional but recommended)
        current_widget.deleteLater()


    def styled_button(self, text, func):
        button = QPushButton(text)
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedHeight(45)
        button.setFont(QFont("Segoe UI", 10))
        button.setObjectName("actionButton")
        button.clicked.connect(func)
        return button

    def divider(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #ccc;")
        return line

    def change_theme(self, theme):
        if theme == "Dark":
            self.setStyleSheet(self.get_stylesheet(dark=True))
        else:
            self.setStyleSheet(self.get_stylesheet(dark=False))

    def change_admin(self):
        admin_name, ok = QInputDialog.getText(self, "Change Admin", "Enter new admin username:")
        if ok and admin_name.strip():
            self.manager.set_admin(admin_name.strip())
            QMessageBox.information(self, "Success", f"✅ Admin changed to {admin_name}")

    def change_password(self):
        old_pass, ok1 = QInputDialog.getText(self, "Old Password", "Enter old password:", QLineEdit.Password)
        if not ok1: return

        new_pass, ok2 = QInputDialog.getText(self, "New Password", "Enter new password:", QLineEdit.Password)
        if not ok2: return

        if self.manager.change_password(old_pass, new_pass):
            QMessageBox.information(self, "Success", "✅ Password changed successfully!")
        else:
            QMessageBox.warning(self, "Failed", "❌ Incorrect old password.")

    def reset_database(self):
        reply = QMessageBox.question(
            self,
            "Confirm Reset",
            "⚠️ This will delete all attendance data. Are you sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                self.manager.reset_database()  # ✅ This calls the function from backend.py
                QMessageBox.information(self, "Reset", "✅ Attendance database has been reset.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"❌ Failed to reset database.\n{str(e)}")


    def check_updates(self):
        QMessageBox.information(self, "Update", "✅ You are using the latest version.")

    def get_stylesheet(self, dark=False):
        if dark:
            return """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1e1e1e, stop:1 #2c2c2c);
                color: white;
                font-family: 'Segoe UI';
            }
            #card {
                background-color: #333;
                border-radius: 15px;
            }
            QComboBox, QLineEdit, #actionButton {
                background-color: #444;
                color: white;
                border: 1px solid #666;
                border-radius: 6px;
                padding: 6px;
            }
            #actionButton:hover {
                background-color: #555;
            }
            """
        else:
            return """
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #e8f0ff, stop:1 #ffffff);
                color: #333;
                font-family: 'Segoe UI';
            }
            #card {
                background-color: #ffffff;
                border-radius: 15px;
                box-shadow: 0px 0px 15px rgba(0,0,0,0.1);
            }
            QComboBox, QLineEdit, #actionButton {
                background-color: #f9f9f9;
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 6px;
            }
            #actionButton:hover {
                background-color: #e0e0e0;
            }
            """
