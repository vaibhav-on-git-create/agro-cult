import sys

sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from path_storage_info import request_path
from data_tools import json_tool

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtGui import QFont, QPixmap, QPainter
from PyQt6.QtCore import Qt


class AgroCultApp(QWidget):
    def __init__(
        self,
        bg_image_path=r"E:\AGROCULT UI\MAINPAGE\MAIN_BACKGROUND.jpg"
    ):
        super().__init__()
        self.bg_image_path = bg_image_path
        self.bg_pixmap = QPixmap(self.bg_image_path) if self.bg_image_path else None
        self.initUI()

    def paintEvent(self, event):
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            painter = QPainter(self)
            painter.setOpacity(0.5)  # translucent background effect
            painter.drawPixmap(self.rect(), self.bg_pixmap)
        super().paintEvent(event)

    def initUI(self):
        self.setWindowTitle('Agro-Cult')
        self.setGeometry(100, 100, 1200, 600)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_layout = QHBoxLayout()
        title_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("AGRO-CULT")
        title.setFont(QFont("Arial", 60, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")

        icon_label = QLabel()
        icon_label.setText("🌱")
        icon_label.setFont(QFont("Arial", 40))

        title_layout.addWidget(title)
        title_layout.addWidget(icon_label)

        subtitle = QLabel(
            "Connecting farmers and buyers through transparent pricing, "
            "real-time demand analysis, and sustainable agriculture"
        )
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: white;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setContentsMargins(50, 10, 50, 40)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        farmer_btn = QPushButton("  🌱  I'm a Farmer")
        buyer_btn = QPushButton("   🛒  I'm a Buyer")

        button_style = """
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2cae73, stop:1 #57a1f8
                );
                border: 2px solid #1e7f46;
                border-radius: 8px;
                padding: 12px 30px;
                color: white;
                font-weight: 900;
                font-size: 16px;
                min-width: 140px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #27a364, stop:1 #4f91e4
                );
                border-color: #146021;
            }
            QPushButton:pressed {
                background-color: #1b5e35;
                border-color: #0f3a1a;
            }
        """

        farmer_btn.setStyleSheet(button_style)
        buyer_btn.setStyleSheet(button_style)

        buttons_layout.addWidget(farmer_btn)
        buttons_layout.addWidget(buyer_btn)

        main_layout.addLayout(title_layout)
        main_layout.addWidget(subtitle)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        # Connect button clicks to the new method
        farmer_btn.clicked.connect(lambda: self.on_button_clicked("I'm a Farmer"))
        buyer_btn.clicked.connect(lambda: self.on_button_clicked("I'm a Buyer"))
    
    def on_button_clicked(self, role):
        """Prints a message to the console when a button is clicked."""
        print(f"The '{role}' button was clicked.")
        if role =="I'm a Farmer":
            from servers.login.farmer_login import FarmerLoginPage
            self.login_farmer = FarmerLoginPage()
            self.login_farmer.show()
            
        if role=="I'm a Buyer":
            from servers.login.buyer_login import BuyerLoginPage
            self.login_buyer = BuyerLoginPage()
            self.login_buyer.show()

if __name__ == '__main__':
    bg_image_path = r"../agro-cult/media/Main_page/MAIN_BACKGROUND.jpg"
    app = QApplication(sys.argv)
    window = AgroCultApp(bg_image_path)
    window.show()
    sys.exit(app.exec())
