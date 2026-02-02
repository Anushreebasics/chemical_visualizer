from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QFrame,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette

from api import APIClient
from styles import STYLESHEET, StyleHelper


class LoginDialog(QDialog):
    """Modern Login/Register Dialog with Dark Theme."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.token = None
        self.user = None
        self.init_ui()
        
        # Center on screen
        screen_geometry = self.screen().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
        # Apply palette for elements not covered by stylesheet
        StyleHelper.set_dark_palette(self)

    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(0, 0, 480, 550)
        # Custom Stylesheet for Login Dialog (overrides global dark theme)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #667eea, stop:1 #764ba2);
            }
            QFrame#card {
                background-color: #ffffff;
                border-radius: 12px;
                border: none;
            }
            QLabel {
                color: #333333;
                font-family: 'Inter', sans-serif;
            }
            QLabel#headerTitle {
                font-size: 28px;
                font-weight: 700;
                color: #667eea;
                margin-bottom: 8px;
            }
            QLabel#subText {
                font-size: 14px;
                color: #666666;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 10px 14px;
                color: #1e293b;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #667eea;
            }
            QPushButton#primaryBtn {
                background-color: #667eea;
                color: white;
                border-radius: 10px;
                font-weight: 600;
                border: none;
            }
            QPushButton#primaryBtn:hover {
                background-color: #5a67d8;
            }
            QPushButton {
                 color: #667eea;
                 font-weight: 600;
                 background: transparent;
                 border: none;
            }
            QPushButton:hover {
                background: transparent;
                text-decoration: underline;
            }
        """)

        # Main Layout
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setAlignment(Qt.AlignCenter)

        # Card Container
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        card = QFrame()
        card.setObjectName("card")
        card.setFixedWidth(400)
        
        # Shadow for card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 10)
        card.setGraphicsEffect(shadow)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Titles
        title = QLabel('Chemical Equipment\nVisualizer')
        title.setObjectName("headerTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        sub_title = QLabel('Login')
        sub_title.setStyleSheet("font-size: 24px; font-weight: 600; color: #333; margin-bottom: 20px;")
        sub_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub_title)

        # Form
        username_label = QLabel('Username')
        username_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #94a3b8; margin-bottom: 4px;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        layout.addWidget(self.username_input)

        password_label = QLabel('Password')
        password_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #94a3b8; margin-bottom: 4px; margin-top: 10px;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        layout.addSpacing(20)

        # Buttons
        login_btn = QPushButton('Login')
        login_btn.setObjectName("primaryBtn")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setMinimumHeight(45)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        # Register Link (Bottom)
        reg_layout = QHBoxLayout()
        reg_layout.setAlignment(Qt.AlignCenter)
        reg_lbl = QLabel("Don't have an account?")
        reg_lbl.setStyleSheet("color: #666; font-size: 13px;")
        
        register_btn = QPushButton('Register here')
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.clicked.connect(self.handle_register)
        
        reg_layout.addWidget(reg_lbl)
        reg_layout.addWidget(register_btn)
        layout.addLayout(reg_layout)

        root_layout.addWidget(card)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Validation Error', 'Please enter username and password')
            return

        try:
            client = APIClient()
            response = client.login(username, password)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.user = data.get('user')
                self.accept()
            else:
                error_msg = response.json().get('error', 'Login failed')
                QMessageBox.warning(self, 'Login Failed', error_msg)
        except Exception as exc:
            QMessageBox.critical(self, 'Connection Error', f'Failed to connect: {exc}')

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, 'Validation Error', 'Please enter username and password')
            return

        try:
            client = APIClient()
            response = client.register(username, '', password)
            if response.status_code == 201:
                data = response.json()
                self.token = data.get('token')
                self.user = data.get('user')
                QMessageBox.information(self, 'Success', 'Registration successful! Logging in...')
                self.accept()
            else:
                error_msg = response.json().get('error', 'Registration failed')
                QMessageBox.warning(self, 'Registration Failed', error_msg)
        except Exception as exc:
            QMessageBox.critical(self, 'Connection Error', f'Failed to connect: {exc}')
