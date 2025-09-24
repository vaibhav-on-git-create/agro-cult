import sys
sys.path.insert(1,"../agro-cult")

from system_bridge import bridge
bridge.bridge_to_all()
from data_tools import json_tool
from path_storage_info import request_path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QHBoxLayout, QVBoxLayout, QGroupBox, QScrollArea
)
from PyQt6.QtGui import QFont, QPixmap, QPainter, QIcon
from PyQt6.QtCore import Qt
buyer_detail_path =request_path.get_path(path_name="buyer_details")
details=json_tool.read_json(file_path=buyer_detail_path)
name=details["name"]

transaction_details_path=request_path.get_path(path_name="buyer_transaction_balance")
balance=len(json_tool.list_json_key(transaction_details_path))

class CropMarketplace(QWidget):
    """
    A PyQt6 application for a crop marketplace with a modern and clean UI.
    Features include a searchable list of featured crops and a translucent
    background effect.
    """
    def __init__(self, bg_image_path=None, agro_coin_image_path=None):
        super().__init__()
        self.setWindowTitle("Quality Crops Marketplace")
        self.setGeometry(200, 100, 1000, 900)
        self.bg_image_path = bg_image_path
        self.agro_coin_image_path = agro_coin_image_path
        
        # Load background image. Note: The image path is not hardcoded here.
        # It's passed to the constructor.
        self.bg_pixmap = QPixmap(self.bg_image_path) if self.bg_image_path else None
        
        # Enable background translucency and set main stylesheet
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(self.get_main_stylesheet())

        self.featured_crop_widgets = [] # List to hold crop widgets for filtering
        self.initUI()
        
    def paintEvent(self, event):
        """Draws a translucent background image if a path is provided."""
        if self.bg_pixmap and not self.bg_pixmap.isNull():
            painter = QPainter(self)
            painter.setOpacity(0.25)  # Adjust background image translucency
            painter.drawPixmap(self.rect(), self.bg_pixmap)
            painter.end()
        super().paintEvent(event)

    def initUI(self):
        """Initializes all UI components and layouts."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)

        # Header Section
        header = QLabel("Quality Crops Marketplace 🛒")
        header.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_desc = QLabel("Discover fresh, high-quality crops directly from verified farmers across India")
        header_desc.setFont(QFont("Arial", 14))

        header_layout = QVBoxLayout()
        header_layout.addWidget(header)
        header_layout.addWidget(header_desc)
        main_layout.addLayout(header_layout)

        main_layout.addSpacing(20)

        # Breadcrumb & Buyer Details
        breadcrumb = QLabel("🏠 Buyer Marketplace")
        breadcrumb.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        breadcrumb.setContentsMargins(5, 0, 0, 5)
        main_layout.addWidget(breadcrumb)

        buyer_name = QLabel(f"Hello {name} ")
        buyer_name.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        buyer_country = QLabel(details["country"])
        buyer_country.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        buyer_details_layout = QVBoxLayout()
        buyer_details_layout.addWidget(buyer_name)
        buyer_details_layout.addWidget(buyer_country)
        buyer_details_layout.setContentsMargins(5, 0, 0, 15)
        main_layout.addLayout(buyer_details_layout)
        
        # Account Balance Section
        balance_group = QGroupBox()
        balance_group.setTitle("Account Balance")
        balance_group.setStyleSheet("""
            QGroupBox { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #a5d6a7, stop:1 #c8e6c9);
                border-radius: 8px;
                padding-top: 20px;
                border: 1px solid #cddc39;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #558b2f;
                font-weight: bold;
            }
        """)

        # Mock balance data and conversion
        agro_coins = balance
        usd_balance = (agro_coins * 100) / 83.0 # Assuming 1 USD = 83 INR
        
        balance_layout = QHBoxLayout()

        # Agro-coin display with optional image
        agro_coin_layout = QHBoxLayout()
        if self.agro_coin_image_path:
            agro_coin_pixmap = QPixmap(self.agro_coin_image_path).scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            agro_coin_label = QLabel()
            agro_coin_label.setPixmap(agro_coin_pixmap)
            agro_coin_layout.addWidget(agro_coin_label)
        
        agro_balance_label = QLabel(f"<span style='font-size: 28px; font-weight: bold; color: #ffffff;'>{agro_coins}</span> <span style='font-size: 12px;font-weight: bold; color: #ffd700;'>Agro-coins</span>")
        agro_coin_layout.addWidget(agro_balance_label)
        agro_coin_layout.addStretch()

        # USD balance display
        usd_balance_layout = QHBoxLayout()
        usd_balance_label = QLabel(f"<span style='font-size: 28px; font-weight: bold; color: #ffffff;'>${usd_balance:.2f}</span> <span style='font-size: 12px; font-weight: bold; color: #ffd700;'>USD</span>")
        usd_balance_layout.addWidget(usd_balance_label)
        usd_balance_layout.addStretch()
        
        balance_layout.addLayout(agro_coin_layout)
        balance_layout.addSpacing(20)
        balance_layout.addLayout(usd_balance_layout)
        balance_layout.addStretch()
        
        # Add "Add Agro-coins" button
        add_coins_btn = QPushButton("Add Agro-coins")
        add_coins_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_coins_btn.setProperty("class", "add-coins-btn")
        add_coins_btn.clicked.connect(self.on_add_coins_clicked)
        balance_layout.addWidget(add_coins_btn)
        
        balance_group.setLayout(balance_layout)
        main_layout.addWidget(balance_group)
        main_layout.addSpacing(20)

        # Search Section
        search_layout = QHBoxLayout()
        search_title = QLabel("Find Quality Crops 🔍")
        search_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        search_title.setStyleSheet("color: #c8e6c9; font-size: 11pt;") # Re-apply style
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search crops, locations, or farmers...")
        self.search_bar.setMinimumHeight(30)
        self.search_bar.textChanged.connect(self.on_search_text_changed)

        filter_button = QPushButton("Advanced Filters")
        filter_button.setFixedHeight(30)
        filter_button.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Add all search elements to a single layout for proper alignment
        search_layout_container = QVBoxLayout()
        search_layout_container.addWidget(search_title)
        
        search_box_layout = QHBoxLayout()
        search_box_layout.addWidget(self.search_bar)
        search_box_layout.addWidget(filter_button)
        search_box_layout.addStretch()

        search_layout_container.addLayout(search_box_layout)
        main_layout.addLayout(search_layout_container)

        # Tags
        tags_layout = QHBoxLayout()
        tags_layout.setSpacing(10)
        tags = ["Rice", "Wheat", "Soybeans", "Organic", "Grade A"]
        for tag in tags:
            btn = QPushButton(tag)
            btn.setEnabled(False) # Tags are for display, not interactive
            btn.setFixedHeight(28)
            tags_layout.addWidget(btn)
        tags_layout.addStretch()
        main_layout.addLayout(tags_layout)

        main_layout.addSpacing(30)

        # Main Cards Section
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(30)

        # Add info cards and install event filter for hover animations
        info_card1 = self.create_info_card(
            "📋 Browse by Category",
            "Explore crops by type - grains, pulses, oilseeds, and more. Find exactly what you need for your business.",
            "Browse Categories", "btn-browse")
        cards_layout.addWidget(info_card1)

        info_card2 = self.create_info_card(
            "💼 Bulk Purchase Deals",
            "Special pricing for large orders! Get better rates on bulk purchases and secure your supply chain.\n\n5% extra discount",
            "View Bulk Deals", "btn-bulk")
        cards_layout.addWidget(info_card2)

        info_card3 = self.create_info_card(
            "⭐ Trusted Farmer Network",
            "Connect with verified, top-rated farmers. Quality guaranteed with transparent ratings and reviews.",
            "View Top Farmers", "btn-trusted")
        cards_layout.addWidget(info_card3)
            
        main_layout.addLayout(cards_layout)

        main_layout.addSpacing(40)

        # Featured Quality Crops Section
        featured_label = QLabel("Featured Quality Crops 🌟")
        featured_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        main_layout.addWidget(featured_label)
        main_layout.addSpacing(10)

        self.crops_layout = QHBoxLayout()
        self.crops_layout.setSpacing(30)
        self.load_featured_crops()
        
        main_layout.addLayout(self.crops_layout)
        main_layout.addStretch()

        # Market Insights Section
        market_group = QGroupBox()
        market_layout = QVBoxLayout()
        market_group.setProperty("class", "market-insights")

        market_label = QLabel("📊 Market Insights")
        market_label.setFont(QFont("Arial", 12, QFont.Weight.ExtraBold))
        market_text = QLabel("Current market conditions show strong demand for organic grains. Prices are 8% above last month's average.")
        market_text.setWordWrap(True)
        market_button = QPushButton("View Detailed Market Report")
        market_button.setCursor(Qt.CursorShape.PointingHandCursor)

        market_layout.addWidget(market_label)
        market_layout.addWidget(market_text)
        market_layout.addWidget(market_button)
        market_group.setLayout(market_layout)

        main_layout.addWidget(market_group)
        
        # Scroll Area for overflow
        scroll_area = QScrollArea()
        container = QWidget()
        container.setLayout(main_layout)
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")

        final_layout = QVBoxLayout()
        final_layout.addWidget(scroll_area)
        self.setLayout(final_layout)
        
    def load_featured_crops(self):
        """Dynamically loads and adds featured crop cards to the UI."""
        crops = [
            {
                "name": "Premium Basmati Rice", "location": "Punjab", "farmer": "Rajesh Kumar",
                "price": "₹3,200/quintal", "msp": "₹2,870", "rating": "4.8",
                "grade": "Grade A", "qty": "50 quintals available", "badge": "Above MSP"
            },
            {
                "name": "Organic Wheat", "location": "Haryana", "farmer": "Meera Devi",
                "price": "₹2,650/quintal", "msp": "₹2,425", "rating": "4.9",
                "grade": "Organic Certified", "qty": "100 quintals available", "badge": "Above MSP"
            },
            {
                "name": "Fresh Soybeans", "location": "Madhya Pradesh", "farmer": "Amit Patel",
                "price": "₹4,100/quintal", "msp": "₹4,000", "rating": "4.7",
                "grade": "Premium", "qty": "75 quintals available", "badge": "Above MSP"
            },
        ]
        
        for crop_data in crops:
            card_widget = self.create_crop_card(crop_data)
            self.featured_crop_widgets.append(card_widget)
            self.crops_layout.addWidget(card_widget)

    def create_info_card(self, title, desc, button_text, button_class):
        """Creates a generic info card widget."""
        card = QGroupBox()
        card.setFixedWidth(300)
        card.setProperty("class", "info-card")
        
        card_layout = QVBoxLayout()
        card_layout.setSpacing(12)
        
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        desc_lbl = QLabel(desc)
        desc_lbl.setWordWrap(True)

        button = QPushButton(button_text)
        button.setFixedHeight(35)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setProperty("class", button_class)

        card_layout.addWidget(title_lbl)
        card_layout.addWidget(desc_lbl)
        card_layout.addStretch()
        card_layout.addWidget(button)
        card.setLayout(card_layout)
        return card

    def create_crop_card(self, crop):
        """Creates a featured crop card widget from a dictionary of data."""
        card = QGroupBox()
        card.setFixedWidth(300)
        card.setProperty("class", "crop-card")
        
        card_layout = QVBoxLayout()
        card_layout.setSpacing(8)

        # Title and Badge
        badge = QLabel(crop["badge"])
        badge.setProperty("class", "badge")
        title_layout = QHBoxLayout()
        crop_name = QLabel(crop["name"])
        crop_name.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title_layout.addWidget(crop_name)
        title_layout.addStretch()
        title_layout.addWidget(badge)
        card_layout.addLayout(title_layout)

        # Details
        crop_loc_farm = QLabel(f"📍 {crop['location']} • {crop['farmer']}")
        crop_loc_farm.setProperty("class", "crop-details-label")
        card_layout.addWidget(crop_loc_farm)
        
        price = QLabel(f"<span style='color:#a5d6a7; font-weight:bold;'>{crop['price']}</span>  MSP: {crop['msp']}")
        card_layout.addWidget(price)

        rating_grade = QLabel(f"⭐ {crop['rating']} • {crop['grade']}")
        rating_grade.setProperty("class", "crop-details-label")
        card_layout.addWidget(rating_grade)

        qty = QLabel(f"📦 {crop['qty']}")
        qty.setProperty("class", "crop-details-label")
        card_layout.addWidget(qty)

        # Buttons
        buttons_layout = QHBoxLayout()
        contact_btn = QPushButton("Contact Farmer")
        contact_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        contact_btn.setProperty("class", "contact-btn")
        view_details_btn = QPushButton("View Details")
        view_details_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        view_details_btn.setProperty("class", "view-details-btn")
        buttons_layout.addWidget(contact_btn)
        buttons_layout.addWidget(view_details_btn)
        card_layout.addLayout(buttons_layout)
        
        card.setLayout(card_layout)
        # Store the search text for this card
        card.search_text = f"{crop['name']} {crop['location']} {crop['farmer']} {crop['grade']}".lower()
        return card

    def on_search_text_changed(self, text):
        """Filters the featured crop cards based on the search bar text."""
        search_query = text.lower().strip()
        for card in self.featured_crop_widgets:
            if search_query in card.search_text:
                card.show()
            else:
                card.hide()
                
    def on_add_coins_clicked(self):
        """Prints a message when the 'Add Agro-coins' button is clicked."""
        from UI.add_agro_coin import AgroCoinsApp
        self.add_coins_window = AgroCoinsApp()
        self.add_coins_window.show()
        
        print("Add Agro-coins button clicked.")
        
    def get_main_stylesheet(self):
        """Returns the complete stylesheet for the application."""
        return """
            QWidget {
                background: transparent;
                font-family: Arial;
                color: #ffffff; /* Main font color is white */
            }
            QLabel {
                color: #c8e6c9; /* Light green for general labels */
            }
            QLabel[class="crop-details-label"] {
                color: white;
                font-weight: bold;
                font-size: 9pt;
            }
            QLabel[class="badge"] {
                background-color: #66bb6a;
                color: white;
                font-size: 9pt;
                padding: 3px 8px;
                border-radius: 10px;
                max-width: 80px;
                qproperty-alignment: AlignCenter;
            }
            QGroupBox {
                border: none;
                font-weight: bold;
                font-size: 11pt;
            }
            QGroupBox[class="info-card"] {
                background-color: #4caf5080; /* translucent green */
                border-radius: 10px;
                border: 1px solid #388e3c;
                padding: 20px;
            }
            QGroupBox[class="info-card"] QLabel {
                color: white;
                font-weight: bold;
            }
            QGroupBox[class="crop-card"] {
                background-color: #4caf5080; /* translucent green */
                border-radius: 12px;
                border: 1px solid #388e3c;
                padding: 20px;
            }
            QGroupBox[class="crop-card"] QLabel {
                color: white;
                font-weight: bold;
            }
            QGroupBox[class="market-insights"] {
                border-left: 4px solid #4caf50;
                background-color: #a5d6a781; /* light translucent green */
                border-radius: 8px;
                padding: 20px;
            }
            QGroupBox[class="market-insights"] QLabel {
                color: white;
                font-weight: bold;
            }
            QPushButton {
                font-weight: 600;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
            QPushButton[class="add-coins-btn"] {
                background-color: #388e3c;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border: 1px solid #2e7d32;
            }
            QPushButton[class="add-coins-btn"]:hover {
                background-color: #2e7d32;
            }
            QPushButton[class="add-coins-btn"]:pressed {
                background-color: #1b5e20;
            }
            QPushButton[class="btn-browse"], QPushButton[class="btn-bulk"] {
                background-color: #4caf50;
                color: white;
            }
            QPushButton[class="btn-browse"]:hover, QPushButton[class="btn-bulk"]:hover {
                background-color: #388e3c;
            }
            QPushButton[class="btn-browse"]:pressed, QPushButton[class="btn-bulk"]:pressed {
                background-color: #2e7d32;
            }
            QPushButton[class="btn-trusted"] {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4caf50, stop:1 #81c784);
                color: white;
            }
            QPushButton[class="btn-trusted"]:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #388e3c, stop:1 #66bb6a);
            }
            QPushButton[class="btn-trusted"]:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2e7d32, stop:1 #4caf50);
            }
            QPushButton[class="contact-btn"] {
                background-color: #4caf50;
                color: white;
            }
            QPushButton[class="contact-btn"]:hover {
                background-color: #388e3c;
            }
            QPushButton[class="contact-btn"]:pressed {
                background-color: #2e7d32;
            }
            QPushButton[class="view-details-btn"] {
                background-color: #f5f5f5;
                color: #333333;
            }
            QPushButton[class="view-details-btn"]:hover {
                background-color: #e0e0e0;
            }
            QPushButton[class="view-details-btn"]:pressed {
                background-color: #cccccc;
            }
            QPushButton[class="market-insights-btn"] {
                background-color: #4caf50;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
                max-width: 220px;
            }
            QPushButton[class="market-insights-btn"]:hover {
                background-color: #388e3c;
            }
            QPushButton[class="market-insights-btn"]:pressed {
                background-color: #2e7d32;
            }
            QLineEdit {
                border: 2px solid #4caf50;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 14px;
                color: #333333; /* Dark color for input text */
            }
            QLineEdit:focus {
                background-color: #e8f5e9;
            }
            QLineEdit::placeholder {
                color: #cccccc; /* Lighter color for placeholder text */
            }
            QScrollArea {
                background: transparent;
            }
        """

bg_image_path = r"../agro-cult/media/buyer_main_page/BUYER_BACKGROUUND.jpg" # Example: r"C:\path\to\your\image.jpg"
    # To use the new Agro-coin image feature, uncomment the line below and replace
    # 'path/to/your/agro_coin_16x16.png' with a valid path to a 16x16 pixel image.
    # agro_coin_image_path = "path/to/your/agro_coin_16x16.png"
agro_coin_image_path = r"../agro-cult/media/agro-coin/generated-image (1) (1).png" # Placeholder.
if __name__ == "__main__":
    # NOTE: The background image path is now a variable. Please replace it with
    # a valid path on your system, or leave it as None to use no background.
    # On most operating systems, a relative path might look like 'images/background.jpg'.
    app = QApplication(sys.argv)
    window = CropMarketplace(bg_image_path, agro_coin_image_path)
    window.show()
    sys.exit(app.exec())
