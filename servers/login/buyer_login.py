import sys

sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()
from path_storage_info import request_path
from data_tools import json_tool

buyer_details_path = request_path.get_path("buyer_details")
buyer_codex_path = request_path.get_path("buyer_codex")
buyer_id_path = request_path.get_path("buyer_id_register")

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout,
    QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices

class BuyerLoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛒 Buyer Login")
        self.setFixedSize(450, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #e3f2fd, stop:1 #bbdefb);
            }
        """)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # --- Login Card Container ---
        login_card = QWidget()
        login_card.setFixedSize(380, 520)
        login_card.setStyleSheet("""
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
        login_card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(login_card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(15)

        # --- Logo and Header Text ---
        logo_label = QLabel("🛒")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("font-size: 60px; color: #1e88e5;")

        welcome_label = QLabel("Shop with Freshness")
        welcome_label.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("color: #212121;")

        subtitle_label = QLabel("Sign in to find farm-fresh products")
        subtitle_label.setFont(QFont("Segoe UI", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #757575;")

        # --- Input Fields ---
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        username_label.setStyleSheet("color: #424242;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
                background-color: #fafafa;
                color: #212121;
            }
            QLineEdit:focus {
                border: 2px solid #64b5f6;
            }
        """)

        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Weight.DemiBold))
        password_label.setStyleSheet("color: #424242;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFixedHeight(40)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 0 15px;
                font-size: 14px;
                background-color: #fafafa;
                color: #212121;
            }
            QLineEdit:focus {
                border: 2px solid #64b5f6;
            }
        """)

        # --- Forgot Password Button ---
        forgot_password_button = QPushButton("Forgot Password?")
        forgot_password_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2196f3;
                border: none;
                text-align: right;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        forgot_password_button.clicked.connect(self.forgot_password)

        # --- Sign In button ---
        sign_in_button = QPushButton("Sign In")
        sign_in_button.setFixedHeight(50)
        sign_in_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                             stop:0 #ffb74d, stop:1 #ffa000);
                color: #fff;
                border-radius: 10px;
                font-weight: bold;
                font-size: 16px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                             stop:0 #ffc107, stop:1 #fb8c00);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                             stop:0 #f57c00, stop:1 #e65100);
            }
        """)
        sign_in_button.clicked.connect(self.check_login)

        # --- Sign Up Link ---
        sign_up_link = QLabel()
        sign_up_link.setText(
            "<a href='#' style='color: #2196f3; text-decoration: none; font-weight: bold;'>"
            "Don't have an account? Sign Up</a>"
        )
        sign_up_link.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sign_up_link.setOpenExternalLinks(False)
        sign_up_link.linkActivated.connect(self.open_sign_up)

        # --- Add widgets to the card layout ---
        card_layout.addWidget(logo_label)
        card_layout.addWidget(welcome_label)
        card_layout.addWidget(subtitle_label)
        card_layout.addSpacing(25)
        card_layout.addWidget(username_label)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(password_label)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(forgot_password_button)
        card_layout.addSpacing(10)
        card_layout.addWidget(sign_in_button)
        card_layout.addSpacing(10)
        card_layout.addWidget(sign_up_link)

        # Add the login card to the main layout
        main_layout.addWidget(login_card)

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Placeholder for buyer authentication.
        if username == json_tool.read_json(file_path=buyer_details_path)["name"] and \
        password == json_tool.read_json(file_path=buyer_codex_path)[json_tool.read_json(file_path=buyer_details_path)["id"]]:
            
            self.show_message("Success", "Login Successful! Welcome, buyer.", QMessageBox.Icon.Information)
            from UI.buyer import CropMarketplace
            from UI import buyer
            self.buyer_dash = CropMarketplace(buyer.bg_image_path , buyer.agro_coin_image_path)
            self.buyer_dash.show()
        else:
            self.show_message("Error", "Invalid username or password.", QMessageBox.Icon.Warning)

    def show_message(self, title, message, icon):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(icon)
        msg.setStyleSheet("""
            QMessageBox { background-color: #f7fdf5; }
            QLabel { color: #212121; }
            QPushButton {
                background-color: #2196f3;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
        """)
        msg.exec()
    
    def forgot_password(self):
        self.show_message("Forgot Password", "A password reset link has been sent to your email.",
                          QMessageBox.Icon.Information)

    def open_sign_up(self):
        # self.show_message("Sign Up", "Redirecting to the sign-up page...",
        #                   QMessageBox.Icon.Information)
        from servers.login.registration_page import SignUpPage
        self.buyer_sign_up = SignUpPage()
        self.buyer_sign_up.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuyerLoginPage()
    window.show()
    sys.exit(app.exec())