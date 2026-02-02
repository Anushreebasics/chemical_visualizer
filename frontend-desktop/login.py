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
        
        # Apply palette for elements not covered by stylesheet
        StyleHelper.set_dark_palette(self)

    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(0, 0, 480, 550)
        self.setStyleSheet(STYLESHEET)
        
        # Center on screen (approximate if no parent)
        if self.parent():
            self.move(self.parent().window().frameGeometry().center() - self.rect().center())

        # Main Layout
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setAlignment(Qt.AlignCenter)

        # Card Container
        card = StyleHelper.create_card_frame()
        card.setFixedWidth(380)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(24)

        # Logo (Text based)
        logo_label = QLabel('CE')
        logo_label.setStyleSheet("font-size: 48px; font-weight: 800; color: #6366f1; margin-bottom: 5px;")
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Titles
        title = QLabel('ChemViz')
        title.setObjectName("headerTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel('Sign in to access your dashboard')
        subtitle.setObjectName("subText")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        # Form
        username_label = QLabel('Username')
        username_label.setObjectName("subText")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter your username')
        layout.addWidget(self.username_input)

        password_label = QLabel('Password')
        password_label.setObjectName("subText")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Enter your password')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        layout.addSpacing(20)

        # Buttons
        login_btn = QPushButton('Sign In')
        login_btn.setObjectName("primaryBtn")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setMinimumHeight(45)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)

        # Divider
        div_layout = QHBoxLayout()
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setStyleSheet("color: #334155;")
        lbl = QLabel("OR")
        lbl.setStyleSheet("color: #475569; font-size: 11px;")
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setStyleSheet("color: #334155;")
        
        div_layout.addWidget(line1)
        div_layout.addWidget(lbl)
        div_layout.addWidget(line2)
        layout.addLayout(div_layout)

        register_btn = QPushButton('Create Account')
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setMinimumHeight(45)
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)

        layout.addStretch()
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
