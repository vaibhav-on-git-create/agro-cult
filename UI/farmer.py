import sys

sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()

from path_storage_info import request_path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap, QPainter
import webbrowser

class FarmerDashboard(QWidget):
    def __init__(self, bg_image_path=None):
        super().__init__()
        self.setWindowTitle("Farmer Dashboard")
        self.resize(1000, 900)
        self.bg_image_path = bg_image_path
        self.bg_pixmap = QPixmap(self.bg_image_path) if self.bg_image_path else None
        self.farmer_gpt_window = None  # To hold a reference to the new window
        self.initUI()

    def paintEvent(self, event):
        # Paint background image for the whole widget
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            painter = QPainter(self)
            painter.setOpacity(0.45)
            scaled = self.bg_pixmap.scaled(
                self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(self.rect(), scaled)
        super().paintEvent(event)

    def add_cards_row(self, main_layout, card_widgets):
        row_layout = QHBoxLayout()
        row_layout.setSpacing(24)
        row_layout.setContentsMargins(12, 12, 12, 12)
        for card in card_widgets:
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            row_layout.addWidget(card)
        row_container = QWidget()
        row_container.setLayout(row_layout)
        scroll_row = QScrollArea()
        scroll_row.setWidgetResizable(True)
        scroll_row.setWidget(row_container)
        scroll_row.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_row.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_row.setStyleSheet("background: transparent;")
        main_layout.addWidget(scroll_row)

    def on_button_click(self, button_text):
        """Prints the name of the button that was clicked."""
        print(f"Button Clicked: {button_text}")
        if button_text == "View Demand Trends":
            from system_files.analyzers.get_demand import AgroCultReportApp
            self.demand_window = AgroCultReportApp()
            self.demand_window.show()

    def initUI(self):
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(22)
        main_layout.setContentsMargins(22, 22, 22, 22)
        scroll_area.setWidget(container)
        scroll_area.setStyleSheet("background: transparent;")

        # Header
        header = QFrame()
        header.setStyleSheet("""
            background-color: #2cae73;
            border-radius: 18px;
        """)
        header.setFixedHeight(140)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(40, 32, 40, 28)
        back_label = QLabel("←  Back to Home")
        back_label.setStyleSheet("color: white; font-weight: 600; font-size: 14px;")
        back_label.setCursor(Qt.CursorShape.PointingHandCursor)
        title_lbl = QLabel("Welcome Back, Farmer! 🌾")
        title_lbl.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: white;")
        subtitle_lbl = QLabel("You're one step closer to better crop prices!")
        subtitle_lbl.setStyleSheet("color: white; font-size: 13px;")
        header_layout.addWidget(back_label)
        header_layout.addWidget(title_lbl)
        header_layout.addWidget(subtitle_lbl)
        main_layout.addWidget(header)

        # Breadcrumb
        breadcrumb = QFrame()
        breadcrumb.setStyleSheet("""
            background-color: #eaf6f2;
            border-radius: 10px;
        """)
        breadcrumb.setFixedHeight(40)
        breadcrumb_layout = QHBoxLayout(breadcrumb)
        breadcrumb_layout.setContentsMargins(15, 5, 15, 5)
        home_icon = QLabel("🏠")
        home_icon.setFixedWidth(22)
        breadcrumb_layout.addWidget(home_icon, alignment=Qt.AlignmentFlag.AlignLeft)
        breadcrumb_label = QLabel("Farmer Dashboard")
        breadcrumb_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #1e7f46;")
        breadcrumb_layout.addWidget(breadcrumb_label)
        breadcrumb_layout.addStretch()
        main_layout.addWidget(breadcrumb)

        # Stats Cards Row
        stats_data = [
            ("📦", "Active Listings", "12", "Crops for sale", "#2cae73"),
            ("💲", "Avg Price", "₹2,850", "Per quintal", "#2cae73"),
            ("📈", "Market Trend", "+5.2%", "This week", "#57a1f8"),
            ("💰", "Financial Health", "Excellent", "Above MSP sales", "#57a1f8")
        ]
        stats_cards = [self.create_stat_card(*data) for data in stats_data]
        self.add_cards_row(main_layout, stats_cards)

        # Function Cards Row 1
        func_cards_data = [
            ("🤖", "AI Farming Assistant", "24/7 Available", "Get advice from smart farming AI on crops, pests, markets, weather.", "Chat with AI Assistant", "#2cae73", "#57a1f8"),
            ("🏷️", "Upload Crop Stock", "Ready to sell", "List your harvest with photos, quality and quantity.", "Upload Stock", "#2cae73", "#2cae73"),
            ("📊", "Market Rates", "Updated hourly", "See real-time MSP and market rates.", "Check MSP Rates", "#57a1f8", "#57a1f8")
        ]
        func_cards1 = [self.create_func_card(*data) for data in func_cards_data]
        self.add_cards_row(main_layout, func_cards1)
        
        # Connect AI button and add print statement
        self.ai_card = func_cards1[0] # Get the first card (AI assistant)
        ai_button = self.ai_card.findChild(QPushButton)
        ai_button.clicked.connect(lambda: self.on_button_click(ai_button.text()))
        ai_button.clicked.connect(self.chat_with_ai)
        
        # Connect other buttons from the first row
        upload_button = func_cards1[1].findChild(QPushButton)
        upload_button.clicked.connect(lambda: self.on_button_click(upload_button.text()))
        
        market_button = func_cards1[2].findChild(QPushButton)
        market_button.clicked.connect(lambda: self.on_button_click(market_button.text()))

        # Function Cards Row 2
        func_cards_data_2 = [
            ("📉", "Demand Analysis", "", "See high demand crops, plan harvest.", "View Demand Trends", "#2cae73", "#57a1f8"),
            ("✏️", "Manage Listings", "", "Update prices, crop details, mark sold.", "Manage Listings", "#2cae73", "#2cae73"),
            ("💬", "Buyer Messages", "3 new messages", "Negotiate prices, arrange delivery.", "View Messages", "#57a1f8", "#57a1f8")
        ]
        func_cards2 = [self.create_func_card(*data) for data in func_cards_data_2]
        self.add_cards_row(main_layout, func_cards2)
        
        # Connect buttons from the second row
        demand_button = func_cards2[0].findChild(QPushButton)
        demand_button.clicked.connect(lambda: self.on_button_click(demand_button.text()))
        
        manage_button = func_cards2[1].findChild(QPushButton)
        manage_button.clicked.connect(lambda: self.on_button_click(manage_button.text()))
        
        messages_button = func_cards2[2].findChild(QPushButton)
        messages_button.clicked.connect(lambda: self.on_button_click(messages_button.text()))

        # Analytics Card Row (single card, centered)
        analytics_card = self.create_func_card(
            "📈", "Sales Analytics", "", "Track sales, revenue and compare with market prices. Insights to boost your earnings!", "View Analytics", "#2cae73", "#57a1f8"
        )
        analytics_row_layout = QHBoxLayout()
        analytics_row_layout.addStretch()
        analytics_card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        analytics_card.setFixedSize(290, 170)
        analytics_row_layout.addWidget(analytics_card)
        analytics_row_layout.addStretch()
        analytics_row = QWidget()
        analytics_row.setLayout(analytics_row_layout)
        main_layout.addWidget(analytics_row)

        # Connect analytics button
        analytics_button = analytics_card.findChild(QPushButton)
        analytics_button.clicked.connect(lambda: self.on_button_click(analytics_button.text()))

        # Footer Card Row (single, centered and large text)
        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_card = QFrame()
        footer_card.setStyleSheet("""
            border-left: 5px solid #2cae73;
            border-radius: 13px;
            background-color: white;
        """)
        footer_card.setFixedHeight(85)
        footer_text_layout = QHBoxLayout(footer_card)
        footer_text_layout.setContentsMargins(22, 15, 22, 15)
        footer_icon = QLabel("🎯")
        footer_icon.setFont(QFont("Arial", 20))
        footer_icon.setStyleSheet("color: #2cae73; font-weight: 600;")
        footer_text_layout.addWidget(footer_icon)
        footer_text = QLabel(
            "<b style='color:#2cae73;'>You're Doing Great!</b> Crops are 15% above average MSP prices this month. "
            "Upload more premium crops for even higher earnings."
        )
        footer_text.setWordWrap(True)
        footer_text.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        footer_text.setStyleSheet("color: #444444;")
        footer_text_layout.addWidget(footer_text)
        footer_layout.addWidget(footer_card)
        footer_layout.addStretch()
        footer_row = QWidget()
        footer_row.setLayout(footer_layout)
        main_layout.addWidget(footer_row)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll_area)

    def create_stat_card(self, icon, title, bold_text, subtitle, accent_color):
        card = QFrame()
        card.setStyleSheet(f"""
            background-color: white;
            border-radius: 14px;
        """)
        card.setFixedSize(200, 120)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(14, 10, 14, 8)
        row = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet(f"color: {accent_color}; font-size: 17px;")
        icon_lbl.setFixedWidth(24)
        row.addWidget(icon_lbl)
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #1e7f46;")
        row.addWidget(title_lbl)
        row.addStretch()
        card_layout.addLayout(row)
        bold_lbl = QLabel(bold_text)
        bold_lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        bold_lbl.setStyleSheet(f"color: {accent_color};")
        card_layout.addWidget(bold_lbl)
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet("color: #8ea39a; font-size: 11px;")
        card_layout.addWidget(subtitle_lbl)
        return card

    def create_func_card(self, emoji, title, badge, description, button_text, color1, color2):
        card = QFrame()
        card.setFixedSize(290, 170)
        card.setStyleSheet("""
            background-color: white;
            border-radius: 14px;
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(7)
        head_layout = QHBoxLayout()
        emoji_lbl = QLabel(emoji)
        emoji_lbl.setFixedWidth(27)
        emoji_lbl.setStyleSheet("font-size: 20px;")
        head_layout.addWidget(emoji_lbl)
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_lbl.setStyleSheet("color: #1e7f46;")
        head_layout.addWidget(title_lbl)
        head_layout.addStretch()
        layout.addLayout(head_layout)
        if badge:
            badge_lbl = QLabel(badge)
            badge_lbl.setStyleSheet(f"""
                background-color: #eaf6f2;
                color: #2cae73;
                font-size: 10px;
                padding: 2px 12px;
                border-radius: 7px;
                font-weight: 600;
                max-width: 110px;
            """)
            layout.addWidget(badge_lbl)
        desc_lbl = QLabel(description)
        desc_lbl.setWordWrap(True)
        desc_lbl.setStyleSheet("font-size: 12px; color: #666666;")
        layout.addWidget(desc_lbl)
        layout.addStretch()
        button = QPushButton(button_text)
        button.setFixedHeight(35)
        button.setStyleSheet(f"""
            color: white; font-weight: 700;
            border-radius: 8px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 {color1}, stop:1 {color2});
            font-size: 14px;
        """)
        layout.addWidget(button)
        return card
        
    def chat_with_ai(self):
        from servers.farmer_gpt.UI import farmer_gpt
        self.farmer_gpt_window = farmer_gpt.ChatApp()
        self.farmer_gpt_window.show()

bg_image_path = r"../agro-cult/media/farmers_page/FARMERS_BACKGROUND.jpg"
if __name__ == '__main__':
      # Update path as needed
    app = QApplication(sys.argv)
    win = FarmerDashboard(bg_image_path=bg_image_path)
    win.show()
    sys.exit(app.exec())
