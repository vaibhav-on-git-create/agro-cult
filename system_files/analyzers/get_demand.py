import sys

sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from system_files.AI_gatherer.ai_gather import groq_chat_single_query

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QTextEdit,
                             QComboBox)
from PyQt6.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt6.QtCore import Qt
import time

class AgroCultReportApp(QMainWindow):
    """
    A simple PyQt6 application to show a message based on country and state.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agro-Cult Report")
        self.setFixedSize(800, 500)

        # Set the background image
        self.setAutoFillBackground(True)
        palette = self.palette()
        # Use a placeholder path. Replace this with the path to your image file.
        palette.setBrush(QPalette.ColorRole.Window, QBrush(QPixmap("path/to/your/background_image.jpg").scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)))
        self.setPalette(palette)

        # Define simple data to populate the dropdowns
        self.countries_and_states = {
            "India": ["Madhya Pradesh", "Punjab", "Maharashtra", "Gujarat", "Uttar Pradesh", "Telangana"],
            "USA": ["California", "Iowa", "Florida"]
        }

        # Set a professional font
        app_font = QFont("Helvetica", 14)
        self.setFont(app_font)

        # Apply a consistent green theme
        central_widget = QWidget()
        central_widget.setStyleSheet(
            "background-color: #A5D6A7;"
            "border-radius: 20px;"
        )
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel("Agro-Cult Report")
        title_font = QFont("Helvetica", 20)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2E7D32; background-color: transparent;")
        main_layout.addWidget(title_label)
        
        # Dropdowns and Button
        controls_layout = QHBoxLayout()
        
        # Country Dropdown with elegant label
        country_label = QLabel("Country:")
        country_label.setStyleSheet("background-color: #2E7D32; color: white; padding: 5px 12px; border-radius: 15px; font-weight: bold;")
        self.country_combo = QComboBox()
        self.country_combo.addItem("Select Country")
        self.country_combo.addItems(self.countries_and_states.keys())
        self.country_combo.setStyleSheet(
            "QComboBox { border: 2px solid #2E7D32; border-radius: 10px; padding: 8px; background-color: #4CAF50; color: white; }"
            "QComboBox::drop-down { border: none; }"
        )
        self.country_combo.currentIndexChanged.connect(self.update_states)

        # State/Region Dropdown with elegant label
        state_label = QLabel("State/Region:")
        state_label.setStyleSheet("background-color: #2E7D32; color: white; padding: 5px 12px; border-radius: 15px; font-weight: bold;")
        self.state_combo = QComboBox()
        self.state_combo.addItem("Select State/Region")
        self.state_combo.setEnabled(False)
        self.state_combo.setStyleSheet(
            "QComboBox { border: 2px solid #2E7D32; border-radius: 10px; padding: 8px; background-color: #4CAF50; color: white; }"
            "QComboBox::drop-down { border: none; }"
            "QComboBox:disabled { background-color: #D3E9D5; color: #555555; }"
        )

        # Analysis button with shadow and subtle hover effect
        self.analyze_button = QPushButton("Generate Report")
        self.analyze_button.setStyleSheet(
            "QPushButton { background-color: #2E7D32; color: white; border: none; padding: 12px; "
            "border-radius: 10px; font-weight: bold; box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3); }"
            "QPushButton:hover { background-color: #388E3C; }"
            "QPushButton:pressed { background-color: #1B5E20; box-shadow: none; }"
        )
        self.analyze_button.clicked.connect(self.run_analysis)
        
        controls_layout.addWidget(country_label)
        controls_layout.addWidget(self.country_combo)
        controls_layout.addWidget(state_label)
        controls_layout.addWidget(self.state_combo)
        controls_layout.addWidget(self.analyze_button)
        main_layout.addLayout(controls_layout)

        # Report display area
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Helvetica", 16))
        self.report_text.setStyleSheet(
            "border: none; border-radius: 15px; padding: 15px; background-color: #3A3A3A; color: white;"
        )
        main_layout.addWidget(self.report_text)

    def update_states(self):
        self.state_combo.clear()
        self.state_combo.addItem("Select State/Region")
        selected_country = self.country_combo.currentText()
        if selected_country != "Select Country":
            states = self.countries_and_states.get(selected_country, [])
            self.state_combo.addItems(states)
            self.state_combo.setEnabled(True)
        else:
            self.state_combo.setEnabled(False)

    def run_analysis(self):
        country = self.country_combo.currentText()
        state = self.state_combo.currentText()

        if country == "Select Country" or state == "Select State/Region":
            self.report_text.setText("Please select both a country and a state to generate a report.")
            return
        import datetime
        now = datetime.datetime.year
        message = groq_chat_single_query(query=f"""crop demand in  {country} - {state} in {now} what shall i plant this year to get most 
                                         porfit from the global market , answer 10 lines incluing a poper report of market prices and a fair conlutions."""
                                         , response_language="english and hindi sperately and do not mention the language in answer or number the lines")
         # Simulate a delay for analysis
        print("Analyzing...")
        self.report_text.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AgroCultReportApp()
    window.show()
    sys.exit(app.exec())
