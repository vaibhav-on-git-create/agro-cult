import sys
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QGraphicsDropShadowEffect, QScrollArea, QHBoxLayout
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, pyqtSignal

sys.path.insert(1,"../agro-cult")
from system_bridge import bridge
bridge.bridge_to_all()

from data_tools import json_tool
from path_storage_info import request_path

farmer_id_path = request_path.get_path(path_name="farmer_id_register")
buyer_id_path = request_path.get_path(path_name="buyer_id_register")

famer_user_list = json_tool.list_json_key(file_path=farmer_id_path)
buyer_and_farmer_user_list = json_tool.list_json_key(file_path=buyer_id_path)

all_user_list = famer_user_list + buyer_and_farmer_user_list


class SignUpPage(QWidget):
    # Signal to be emitted upon successful registration, passing user data as a dict
    registration_successful = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤝 Create an Account")
        # Set a fixed size for the main window, but allow the inner content to scroll.
        self.setFixedSize(450, 820)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #f0f4f7, stop:1 #e8eaf6);
            }
        """)

        # List of pre-registered users for duplicate checking
        self.registered_users = all_user_list

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the scroll area

        # --- Scroll Area for the form card ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # --- Sign Up Card Container ---
        signup_card = QWidget()
        signup_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 18px;
            }
        """)

        # Add a subtle shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        signup_card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(signup_card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)

        # --- Logo and Header Text ---
        logo_label = QLabel("📝")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 60px; color: #4a5568;")

        welcome_label = QLabel("Create Your Account")
        welcome_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: #2d3748;")

        subtitle_label = QLabel("Join our agro-cult community today")
        subtitle_label.setFont(QFont("Segoe UI", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #718096;")

        # --- Form Fields ---
        # Name
        name_label = QLabel("Full Name")
        name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        name_label.setStyleSheet("color: #4a5568;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        self.name_input.setFixedHeight(40)
        self.name_input.setStyleSheet(self.get_line_edit_style())
        
        # Phone Number
        phone_label = QLabel("Phone Number")
        phone_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        phone_label.setStyleSheet("color: #4a5568;")
        self.phone_number_input = QLineEdit()
        self.phone_number_input.setPlaceholderText("Enter your phone number")
        self.phone_number_input.setFixedHeight(40)
        self.phone_number_input.setStyleSheet(self.get_line_edit_style())
        self.phone_number_input.textChanged.connect(self.validate_phone_number)
        
        # Country Code Dropdown
        self.country_code_combo = QComboBox()
        self.country_code_combo.setFixedHeight(40)
        self.country_code_combo.setStyleSheet(self.get_combo_box_style())
        self.country_code_combo.addItems([
            "+91 (India)", "+1 (USA)", "+44 (UK)", "+86 (China)", "+49 (Germany)"
        ])
        
        # Horizontal layout for phone number and country code
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(self.country_code_combo, 1)
        phone_layout.addWidget(self.phone_number_input, 2)
        

        # Username
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        username_label.setStyleSheet("color: #4a5568;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Create a username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet(self.get_line_edit_style())
        self.username_input.textChanged.connect(self.validate_username)
        
        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        password_label.setStyleSheet("color: #4a5568;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter a password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet(self.get_line_edit_style())
        self.password_input.textChanged.connect(self.validate_password)
        
        # Confirm Password
        confirm_password_label = QLabel("Confirm Password")
        confirm_password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        confirm_password_label.setStyleSheet("color: #4a5568;")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setFixedHeight(40)
        self.confirm_password_input.setStyleSheet(self.get_line_edit_style())
        self.confirm_password_input.textChanged.connect(self.check_passwords_match)
        
        # Country
        country_label = QLabel("Country")
        country_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        country_label.setStyleSheet("color: #4a5568;")
        self.country_combo = QComboBox()
        self.country_combo.setFixedHeight(40)
        self.country_combo.setStyleSheet(self.get_combo_box_style())
        
        # State
        state_label = QLabel("State/Region")
        state_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        state_label.setStyleSheet("color: #4a5568;")
        self.state_combo = QComboBox()
        self.state_combo.setFixedHeight(40)
        self.state_combo.setStyleSheet(self.get_combo_box_style())
        
        # Profession
        profession_label = QLabel("I am a...")
        profession_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        profession_label.setStyleSheet("color: #4a5568;")
        self.profession_combo = QComboBox()
        self.profession_combo.addItems(["", "Farmer", "Buyer"])
        self.profession_combo.setFixedHeight(40)
        self.profession_combo.setStyleSheet(self.get_combo_box_style())
        
        # --- Conditionally Visible Fields ---
        # Scale (for both Farmer and Buyer)
        self.scale_label = QLabel("Scale")
        self.scale_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.scale_label.setStyleSheet("color: #4a5568;")
        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["", "Small", "Large"])
        self.scale_combo.setFixedHeight(40)
        self.scale_combo.setStyleSheet(self.get_combo_box_style())

        # Bank Details (for Buyer only)
        self.bank_name_label = QLabel("Bank Name")
        self.bank_name_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.bank_name_label.setStyleSheet("color: #4a5568;")
        self.bank_combo = QComboBox()
        self.bank_combo.addItems([
            "",
            "State Bank of India",
            "HDFC Bank",
            "ICICI Bank",
            "Axis Bank",
            "Punjab National Bank"
        ])
        self.bank_combo.setFixedHeight(40)
        self.bank_combo.setStyleSheet(self.get_combo_box_style())
        
        self.account_num_label = QLabel("Account Number")
        self.account_num_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.account_num_label.setStyleSheet("color: #4a5568;")
        self.account_num_input = QLineEdit()
        self.account_num_input.setPlaceholderText("Enter your bank account number")
        self.account_num_input.setFixedHeight(40)
        self.account_num_input.setStyleSheet(self.get_line_edit_style())

        self.bank_password_label = QLabel("Bank Password")
        self.bank_password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        self.bank_password_label.setStyleSheet("color: #4a5568;")
        self.bank_password_input = QLineEdit()
        self.bank_password_input.setPlaceholderText("Enter your bank password")
        self.bank_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.bank_password_input.setFixedHeight(40)
        self.bank_password_input.setStyleSheet(self.get_line_edit_style())
        
        # Hide all conditional widgets initially
        self.scale_label.hide()
        self.scale_combo.hide()
        self.bank_name_label.hide()
        self.bank_combo.hide()
        self.account_num_label.hide()
        self.account_num_input.hide()
        self.bank_password_label.hide()
        self.bank_password_input.hide()

        # --- Sign Up Button ---
        signup_button = QPushButton("Sign Up")
        signup_button.setFixedHeight(50)
        signup_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #6366f1, stop:1 #4f46e5);
                color: white;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #818cf8, stop:1 #6366f1);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 #4338ca, stop:1 #3730a3);
            }
        """)
        signup_button.clicked.connect(self.register_user)

        # --- Widget Layout ---
        card_layout.addWidget(logo_label)
        card_layout.addWidget(welcome_label)
        card_layout.addWidget(subtitle_label)
        card_layout.addSpacing(25)
        card_layout.addWidget(name_label)
        card_layout.addWidget(self.name_input)
        card_layout.addWidget(phone_label)
        card_layout.addLayout(phone_layout) # Add the horizontal layout here
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(confirm_password_label)
        card_layout.addWidget(self.confirm_password_input)
        card_layout.addWidget(country_label)
        card_layout.addWidget(self.country_combo)
        card_layout.addWidget(state_label)
        card_layout.addWidget(self.state_combo)
        card_layout.addWidget(profession_label)
        card_layout.addWidget(self.profession_combo)
        # Add the conditional widgets to the layout
        card_layout.addWidget(self.scale_label)
        card_layout.addWidget(self.scale_combo)
        card_layout.addWidget(self.bank_name_label)
        card_layout.addWidget(self.bank_combo)
        card_layout.addWidget(self.account_num_label)
        card_layout.addWidget(self.account_num_input)
        card_layout.addWidget(self.bank_password_label)
        card_layout.addWidget(self.bank_password_input)
        card_layout.addSpacing(15)
        card_layout.addWidget(signup_button)

        scroll_area.setWidget(signup_card)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # --- Data & Connections ---
        self.country_data = {
            "USA": ["California", "Texas", "Florida"],
            "India": ["Maharashtra", "Karnataka", "Tamil Nadu"],
            "UK": ["England", "Scotland", "Wales"],
            "Canada": ["Ontario", "Quebec", "British Columbia"]
        }
        self.country_combo.addItems([""] + sorted(self.country_data.keys()))
        self.country_combo.currentIndexChanged.connect(self.update_states)
        self.profession_combo.currentIndexChanged.connect(self.toggle_scale_visibility)
        
    def get_line_edit_style(self, color="#cbd5e0"):
        return f"""
            QLineEdit {{
                border: 1px solid {color};
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
                background-color: #fafafa;
                color: #2d3748;
            }}
            QLineEdit:focus {{
                border: 2px solid #6366f1;
            }}
        """

    def get_combo_box_style(self):
        return """
            QComboBox {
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
                background-color: #fafafa;
                color: #2d3748;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #cbd5e0;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
            }
            QComboBox::down-arrow {
                image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M7 10l5 5 5-5z' fill='%23718096'/%3E%3C/svg%3E");
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                background-color: white;
                selection-background-color: #e8eaf6;
                color: #2d3748;
            }
        """
        
    def validate_phone_number(self, text):
        # Basic validation for digits only and length between 7 and 15
        if re.fullmatch(r'\d{7,15}', text):
            self.phone_number_input.setStyleSheet(self.get_line_edit_style("#4CAF50")) # Green
        else:
            self.phone_number_input.setStyleSheet(self.get_line_edit_style("#E53935")) # Red
            
    def validate_username(self, text):
        if text in self.registered_users:
            self.username_input.setStyleSheet(self.get_line_edit_style("#E53935")) # Red
        else:
            self.username_input.setStyleSheet(self.get_line_edit_style("#4CAF50")) # Green

    def validate_password(self, text):
        if len(text) >= 8 and any(c.isupper() for c in text) and any(c.islower() for c in text) and any(c.isdigit() for c in text):
            self.password_input.setStyleSheet(self.get_line_edit_style("#4CAF50"))
        else:
            self.password_input.setStyleSheet(self.get_line_edit_style("#E53935"))
        self.check_passwords_match()

    def check_passwords_match(self, text=None):
        if self.password_input.text() == self.confirm_password_input.text() and self.confirm_password_input.text():
            self.confirm_password_input.setStyleSheet(self.get_line_edit_style("#4CAF50"))
        else:
            self.confirm_password_input.setStyleSheet(self.get_line_edit_style("#E53935"))

    def update_states(self, index):
        self.state_combo.clear()
        selected_country = self.country_combo.currentText()
        if selected_country:
            self.state_combo.addItems([""] + self.country_data.get(selected_country, []))

    def toggle_scale_visibility(self, index):
        selected_profession = self.profession_combo.currentText()

        # Hide all conditional fields first
        self.scale_label.hide()
        self.scale_combo.hide()
        self.bank_name_label.hide()
        self.bank_combo.hide()
        self.account_num_label.hide()
        self.account_num_input.hide()
        self.bank_password_label.hide()
        self.bank_password_input.hide()

        # Show fields based on profession
        if selected_profession == "Farmer":
            self.scale_label.show()
            self.scale_combo.show()
        elif selected_profession == "Buyer":
            self.scale_label.show()
            self.scale_combo.show()
            self.bank_name_label.show()
            self.bank_combo.show()
            self.account_num_label.show()
            self.account_num_input.show()
            self.bank_password_label.show()
            self.bank_password_input.show()

    def register_user(self):
        name = self.name_input.text()
        country_code = self.country_code_combo.currentText().split(" ")[0]
        phone_number = self.phone_number_input.text()
        full_phone_number = country_code + phone_number
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        country = self.country_combo.currentText()
        state = self.state_combo.currentText()
        profession = self.profession_combo.currentText()
        scale = self.scale_combo.currentText() if self.profession_combo.currentText() in ["Farmer", "Buyer"] else "N/A"
        
        # Collect bank details only if the profession is "Buyer"
        if profession == "Buyer":
            bank_name = self.bank_combo.currentText()
            account_num = self.account_num_input.text()
            bank_password = self.bank_password_input.text()
        else:
            bank_name = "N/A"
            account_num = "N/A"
            bank_password = "N/A"

        # Validation checks
        if not all([name, phone_number, username, password, confirm_password, country, state, profession]):
            self.show_message("Error", "Please fill out all required fields.", QMessageBox.Icon.Warning)
            return
        
        # New validation for full phone number
        if not re.fullmatch(r'\d{7,15}', phone_number):
            self.show_message("Error", "Please enter a valid phone number (7-15 digits, no spaces or dashes).", QMessageBox.Icon.Warning)
            return
            
        # New validation for bank details if profession is "Buyer"
        if profession == "Buyer" and not all([bank_name, account_num, bank_password]):
            self.show_message("Error", "As a Buyer, please fill out all bank details.", QMessageBox.Icon.Warning)
            return
        
        if username in self.registered_users:
            self.show_message("Error", "This username is already taken. Please choose another one.", QMessageBox.Icon.Warning)
            return

        if not (len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password)):
            self.show_message("Error", "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.", QMessageBox.Icon.Warning)
            return

        if password != confirm_password:
            self.show_message("Error", "Passwords do not match. Please try again.", QMessageBox.Icon.Warning)
            return

        # If all validations pass, show success message, emit signal, and close
        self.show_message("Success", "Account creation successful!\nUse this info to login. :)", QMessageBox.Icon.Information)
        
        user_data = {
            "name": name,
            "phone_number": full_phone_number,
            "username": username,
            "country": country,
            "state": state,
            "profession": profession,
            "scale": scale,
            "bank_name": bank_name,
            "account_number": account_num,
            "bank_password": bank_password
        }
        self.registration_successful.emit(user_data)
        self.close()

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStyleSheet("""
            QMessageBox { background-color: #f7f7f7; }
            QLabel { color: #2d3748; }
            QPushButton {
                background-color: #6366f1;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
        """)
        msg.exec()


def run_ui():
    """
    Runs the PyQt application and returns user data upon successful registration.
    """
    app = QApplication(sys.argv)
    signup_page = SignUpPage()

    # Use a list to hold the data, so it can be modified by the slot
    user_data = []

    # Connect the signal from the signup page to a slot that stores the data and quits
    signup_page.registration_successful.connect(lambda data: (user_data.append(data), app.quit()))

    signup_page.show()
    app.exec()

    # Return the collected user data
    return user_data[0] if user_data else None

from servers.login.verifier import register_login

if __name__ == "__main__":
    registered_data = run_ui()
    if registered_data:
        print("Registration complete. Entered data:")
        for key, value in registered_data.items():
            print(f"- {key.capitalize()}: {value}")

            
            register_login(
            user_name=registered_data["username"],
            passcode=registered_data["bank_password"],  # Using bank password as login passcode for demo
            role=registered_data["profession"],
            scale=registered_data["scale"],
            country=registered_data["country"],
            state=registered_data["state"],
            phone_number=registered_data["phone_number"],  # Placeholder phone number
            bank_account=registered_data["account_number"],
            bank_passcode=registered_data["bank_password"],
            bank_name=registered_data["bank_name"]
        )


    
    else:
        print("Registration was cancelled or failed.")
