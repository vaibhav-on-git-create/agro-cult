
import sys
sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from servers.farmer_gpt._main.main import groq_chat_single_query
import os
import time
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QLineEdit, QPushButton
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer


# Define your background image path here (For chat box only)
BACKGROUND_IMAGE_PATH = r"../agro-cult/media/farmers_page/FARMERS_BACKGROUND.jpg"  # Change this path


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Farmer's GPT")
        self.setMinimumSize(420, 640)
        self.bg_image_path = BACKGROUND_IMAGE_PATH
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e6f0d4; /* Soft green background for main window */
                font-family: Arial, sans-serif;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(22, 22, 22, 22)
        main_layout.setSpacing(14)

        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("🌱 Ask your farming friend, Farmer's GPT 🚜")
        title_label.setFont(QFont('Arial', 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #216a35; margin-bottom: 7px; text-shadow: 0px 2px 8px #bde6bc;")
        header_layout.addWidget(title_label)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont('Arial', 14))

        if self.bg_image_path and os.path.isfile(self.bg_image_path):
            path = self.bg_image_path.replace("\\", "/")
            chat_bg_style = f"""
                background-image: url("{path}");
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
                background-size: cover;
                color: #ffffff; /* White text */
            """
        else:
            print(f"Background image not found at {self.bg_image_path}, using fallback color.")
            chat_bg_style = "background-color: rgba(0, 0, 0, 0.7); color: #ffffff;"  # Dark semi-transparent fallback with white text

        self.chat_display.setStyleSheet(f"""
            QTextEdit {{
                {chat_bg_style}
                border: 2px solid #bee3b9;
                border-radius: 14px;
                padding: 21px;
                box-shadow: 0 4px 14px rgba(44, 90, 44, 0.10);
            }}
        """)
        main_layout.addWidget(self.chat_display)

        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(12)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message...")
        self.input_field.setFont(QFont('Arial', 14))
        self.input_field.setFixedHeight(48)
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255,255,255,0.8);
                border: 2px solid #a4d4a4;
                border-radius: 22px;
                font-style: italic;
                padding: 0 18px;
                color: #2d502d;
            }
            QLineEdit:focus {
                border-color: #348732;
                background-color: rgba(236,255,234,0.9);
            }
        """)
        input_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedSize(88, 48)
        self.send_button.setFont(QFont('Arial', 15, QFont.Weight.ExtraBold))
        self.send_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #8db78a, stop:1 #467346);
                color: white;
                border-radius: 22px;
                font-weight: bold;
                box-shadow: 0 2px 8px rgba(70,130,70,0.1);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #7fae78, stop:1 #395e39);
            }
            QPushButton:pressed {
                background: #71a373;
            }
        """)
        input_layout.addWidget(self.send_button)

        main_layout.addWidget(input_container)

        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
        self.input_field.setFocus()

        QTimer.singleShot(100, lambda: self.chat_display.append(self.format_chat_bubble(
            "Bot",
            "Hello! I'm a simple chat bot and I'm here to demonstrate the UI. How can I help?",
            is_user=False
        )))

    def _wrap_message(self, message: str, max_words_per_line: int = 12) -> str:
        words = message.split()
        wrapped = ""
        count = 0
        for word in words:
            if count >= max_words_per_line:
                wrapped += "<br>" + word + " "
                count = 1
            else:
                wrapped += word + " "
                count += 1
        return wrapped.strip()

    def format_chat_bubble(self, sender, message, is_user):
        timestamp = time.strftime("%H:%M")
        container_align = "left"

        # White text on bubbles with subtle transparent backgrounds for contrast
        if is_user:
            bubble_style = """
                background: rgba(30, 70, 30, 0.7);
                color: #ffffff;
                border-radius: 21px 21px 8px 21px;
                padding: 12px 20px;
                font-weight: 800;
                font-size: 17px;
            """
        else:
            bubble_style = """
                background: rgba(40, 90, 40, 0.5);
                color: #f0f9f0;
                border-radius: 21px 21px 21px 8px;
                padding: 12px 20px;
                font-weight: 700;
                font-size: 17px;
            """

        return f"""
            <div style="margin: 10px 0; text-align: {container_align};">
                <div style="{bubble_style} display: inline-block; max-width: 75%; word-wrap: break-word;">
                    <span style="font-weight: bold; font-size: 15px;">{sender}:</span><br/>
                    <span>{message}</span>
                    <div style="font-size: 12px; color: #d3efd3; margin-top: 6px; text-align: right; font-weight: normal;">{timestamp}</div>
                </div>
            </div>
            <div style="border-bottom: 1px solid rgba(255,255,255,0.2); margin: 10px 0;"></div>
        """

    def send_message(self):
        msg = self.input_field.text().strip()
        if not msg:
            return
        wrapped = self._wrap_message(msg)
        self.chat_display.append(self.format_chat_bubble("You", wrapped, True))
        self.input_field.clear()
        QTimer.singleShot(500, lambda: self.bot_response(msg))

    def bot_response(self, user_msg):
        
        reply = groq_chat_single_query(user_msg.lower())

        wrapped = self._wrap_message(reply)
        self.chat_display.append(self.format_chat_bubble("Bot", wrapped, False))
        self.chat_display.verticalScrollBar().setValue(self.chat_display.verticalScrollBar().maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec())
