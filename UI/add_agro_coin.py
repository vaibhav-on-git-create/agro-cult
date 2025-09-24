import sys

sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from path_storage_info import request_path
from data_tools import json_tool
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QMessageBox, QComboBox, QDialog, QProgressBar
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

account_details_path = request_path.get_path("buyer_transaction_bank")
buyer_details_path = request_path.get_path("buyer_details")
buyer_codex_path = request_path.get_path("buyer_codex")
buyer_id_path = request_path.get_path("buyer_id_register")

account_number = json_tool.read_json(account_details_path)["ac_no"]
user_name = json_tool.read_json(buyer_details_path)["name"]
bank_name = json_tool.read_json(account_details_path)["bank_name"]
bank_password = json_tool.read_json(account_details_path)["passcode"]


# Fixed conversion rates for this application
INR_PER_USD = 83.0
INR_PER_AGRO_COIN = 100

class BankDetailsDialog(QDialog):
    """
    A pop-up dialog to collect bank account information.
    """
    def __init__(self, dummy_db, parent=None):
        super().__init__(parent)
        self.dummy_db = dummy_db
        self.setWindowTitle("Bank Details")
        self.setFixedSize(400, 300)
        self.setStyleSheet(self.get_stylesheet())
        self.init_ui()

    def init_ui(self):
        """Initializes the UI for the bank details dialog."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        title_lbl = QLabel("Enter Bank Details")
        title_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Bank Name Dropdown
        bank_names = [
            "State Bank of India",
            "HDFC Bank",
            "ICICI Bank",
            "Axis Bank",
            "Punjab National Bank"
        ]
        self.bank_combo = QComboBox()
        self.bank_combo.addItems(bank_names)
        self.bank_combo.setMinimumHeight(35)
        
        # Input fields
        self.account_num_input = QLineEdit()
        self.account_num_input.setPlaceholderText("Account Number")
        self.account_num_input.setMinimumHeight(35)
        
        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText("Agro-Cult User ID")
        self.user_id_input.setMinimumHeight(35)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Bank Account Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)

        # Confirm button
        confirm_btn = QPushButton("Confirm")
        confirm_btn.setMinimumHeight(40)
        confirm_btn.clicked.connect(self.validate_and_accept)
        
        layout.addWidget(title_lbl)
        layout.addWidget(self.bank_combo)
        layout.addWidget(self.account_num_input)
        layout.addWidget(self.user_id_input)
        layout.addWidget(self.password_input)
        layout.addWidget(confirm_btn)
        
        self.setLayout(layout)
    
    def validate_and_accept(self):
        """Validates input fields against the dummy database and accepts the dialog if valid."""
        bank_name = self.bank_combo.currentText()
        account_num = self.account_num_input.text()
        user_id = self.user_id_input.text()
        password = self.password_input.text()

        # Check if the user ID exists in our dummy database
        if user_id in self.dummy_db:
            valid_details = self.dummy_db[user_id]
            # Check if all other details match
            if (bank_name == valid_details["bank_name"] and
                account_num == valid_details["account_number"] and
                password == valid_details["bank_password"]):
                self.accept()
            else:
                QMessageBox.warning(self, "Validation Failed", "Incorrect bank details. Please check and try again.")
        else:
            QMessageBox.warning(self, "Validation Failed", "Agro-Cult User ID not found.")
    
    def get_stylesheet(self):
        """Returns the stylesheet for the dialog."""
        return """
            QDialog {
                background-color: #333333;
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                color: #a5d6a7;
            }
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
            QLineEdit, QComboBox {
                background-color: #555555;
                color: white;
                padding: 8px;
                border: 1px solid #777777;
                border-radius: 4px;
            }
        """

class ProgressDialog(QDialog):
    """
    A dialog with a progress bar to show the coin addition process.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adding Coins...")
        self.setFixedSize(300, 150)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # No frame
        self.setStyleSheet(self.get_stylesheet())
        self.init_ui()
        self.progress_value = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)
        self.start_progress()
        
    def init_ui(self):
        """Initializes the UI for the progress dialog."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        label = QLabel("Adding Agro-coins, please wait...")
        label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        layout.addWidget(label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def start_progress(self):
        """Starts the timer to update the progress bar."""
        self.timer.start(50)  # Update every 50 ms

    def update_progress_bar(self):
        """Increments the progress bar value."""
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        
        if self.progress_value >= 100:
            self.timer.stop()
            self.accept()

    def get_stylesheet(self):
        """Returns the stylesheet for the progress dialog."""
        return """
            QDialog {
                background-color: #333333;
                color: white;
                font-family: Arial;
                border: 2px solid #4caf50;
                border-radius: 10px;
            }
            QLabel {
                color: #c8e6c9;
            }
            QProgressBar {
                border: 1px solid #777777;
                border-radius: 5px;
                background-color: #555555;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 5px;
            }
        """

class TransactionSummaryDialog(QDialog):
    """
    A dialog that shows a summary of the successful transaction.
    """
    def __init__(self, num_coins, parent=None):
        super().__init__(parent)
        self.num_coins = num_coins
        self.inr_amount = num_coins * INR_PER_AGRO_COIN
        self.usd_amount = self.inr_amount / INR_PER_USD
        
        self.setWindowTitle("Transaction Summary")
        self.setFixedSize(400, 200)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(self.get_stylesheet())
        self.init_ui()

    def init_ui(self):
        """Initializes the UI for the summary dialog."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        success_label = QLabel("Transaction Successful!")
        success_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        summary_label = QLabel(f"Added: {self.num_coins} Agro-coins\n"
                               f"Total Cost: {self.inr_amount:.2f} INR\n"
                               f"Amount Billed: ${self.usd_amount:.2f} USD")
        summary_label.setFont(QFont("Arial", 12))
        summary_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(success_label)
        layout.addWidget(summary_label)
        self.setLayout(layout)

    def get_stylesheet(self):
        """Returns the stylesheet for the success dialog."""
        return """
            QDialog {
                background-color: #4caf50;
                color: white;
                font-family: Arial;
                border: 2px solid #388e3c;
                border-radius: 10px;
            }
            QLabel {
                color: white;
            }
        """

class AgroCoinsApp(QWidget):
    """
    The main application window that handles the entire workflow
    using a state-based approach.
    """
    def __init__(self):
        super().__init__()
        # Dummy authentication values
        self.dummy_auth_db = {
            json_tool.read_json(file_path=buyer_details_path)["name"]: json_tool.read_json(file_path=buyer_codex_path)[(json_tool.read_json(file_path=buyer_details_path)["id"])]
        }
        # Dummy bank and user details database for verification
        self.dummy_bank_db = {
            json_tool.read_json(file_path=buyer_details_path)["name"]: {
                "bank_name": 
                json_tool.read_json(account_details_path)["bank_name"],
                "account_number": json_tool.read_json(account_details_path)["ac_no"],
                "bank_password": json_tool.read_json(account_details_path)["passcode"],
                
            }
        }
        self.setWindowTitle("Agro-coin System")
        self.setFixedSize(400, 250)
        self.setStyleSheet(self.get_stylesheet())
        self.num_coins = 0
        self.success_dialog = None
        self.init_ui()

    def init_ui(self):
        """Initializes the main window with the login screen."""
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(15)
        
        title_lbl = QLabel("Add Agro-coins")
        title_lbl.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("User Name")
        self.username_input.setMinimumHeight(35)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(35)
        
        get_started_btn = QPushButton("Get Started")
        get_started_btn.setMinimumHeight(40)
        get_started_btn.clicked.connect(self.authenticate_user)
        
        self.layout.addWidget(title_lbl)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(get_started_btn)
        
        self.layout.addStretch()
        self.setLayout(self.layout)

    def clear_layout(self):
        """Removes all widgets from the current layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout_recursively(item.layout())

    def clear_layout_recursively(self, layout):
        """Helper function to recursively clear a layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout_recursively(item.layout())

    def authenticate_user(self):
        """
        Authenticates the user using dummy credentials and proceeds
        to the next step.
        """
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Check against the dummy authentication database
        if self.dummy_auth_db.get(username) == password:
            QMessageBox.information(self, "Success!", "Authentication successful! Proceeding...")
            self.show_coins_input()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password. Please try again.")

    def show_coins_input(self):
        """Switches the UI to the coin input screen."""
        self.clear_layout()
        
        title_lbl = QLabel("How many Agro-coins?")
        title_lbl.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.coins_input = QLineEdit()
        self.coins_input.setPlaceholderText("Enter number of Agro-coins...")
        self.coins_input.setMinimumHeight(35)
        self.coins_input.textChanged.connect(self.update_usd_display)
        
        self.usd_display_lbl = QLabel("Total: $0.00 USD")
        self.usd_display_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.usd_display_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pay_btn = QPushButton("Pay")
        pay_btn.setMinimumHeight(40)
        pay_btn.clicked.connect(self.open_payment_dialog)
        
        self.layout.addWidget(title_lbl)
        self.layout.addWidget(self.coins_input)
        self.layout.addWidget(self.usd_display_lbl)
        self.layout.addWidget(pay_btn)
        
        self.layout.addStretch()

    def update_usd_display(self):
        """Calculates and updates the total USD amount."""
        try:
            self.num_coins = float(self.coins_input.text())
            inr_amount = self.num_coins * INR_PER_AGRO_COIN
            usd_amount = inr_amount / INR_PER_USD
            self.usd_display_lbl.setText(f"Total: ${usd_amount:.2f} USD")
        except ValueError:
            self.usd_display_lbl.setText("Total: $0.00 USD")

    def open_payment_dialog(self):
        """Opens the bank details dialog and handles its result."""
        try:
            if float(self.coins_input.text()) <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid Amount", "Please enter a valid number of Agro-coins.")
            return

        bank_dialog = BankDetailsDialog(self.dummy_bank_db, self)
        bank_result = bank_dialog.exec()
        
        # The .exec() method returns a value indicating how the dialog was closed.
        # QDialog.Accepted is a constant that has the value of 1.
        # We check for this value directly to avoid the AttributeError.
        if bank_result == 1:
            progress_dialog = ProgressDialog(self)
            progress_result = progress_dialog.exec()
            try:

                if progress_result == QDialog.Accepted:
                    # Show the success dialog without blocking the main window
                    self.success_dialog = TransactionSummaryDialog(self.num_coins, self)
                    self.success_dialog.show()
                    
                    # Close the app after 5 seconds to give the user time to see the success message
                    QTimer.singleShot(5000, self.close_app_after_success)
            except:
                from servers.agro_coin_generator.generator import generator
                user_name_main = request_path.get_path("buyer_details")
                generator.generate_agro_coin(user_name=json_tool.read_json(user_name_main)["name"] , coins=int(self.num_coins))
                

    def close_app_after_success(self):
        """Closes the success dialog and the main application window."""
        if self.success_dialog:
            self.success_dialog.close()
        self.close()

    def get_stylesheet(self):
        """Returns the stylesheet for the main window."""
        return """
            QWidget {
                background-color: #333333;
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                color: #a5d6a7;
            }
            QPushButton {
                background-color: #4caf50;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
            QLineEdit {
                background-color: #555555;
                color: white;
                padding: 8px;
                border: 1px solid #777777;
                border-radius: 4px;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgroCoinsApp()
    window.show()
    sys.exit(app.exec())
