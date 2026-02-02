LIGHT_STYLESHEET = """
QWidget {
    font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
    color: #0f172a;
}
QMainWindow, QDialog {
    background-color: #f8fafc;
}
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #f1f5f9);
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #e2e8f0;
    border-color: #94a3b8;
}
QPushButton:pressed {
    background-color: #cbd5e1;
}
QPushButton#primaryBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6366f1, stop:1 #4f46e5);
    border: 1px solid #4338ca;
    color: #ffffff;
}
QPushButton#primaryBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5b5ee6, stop:1 #4338ca);
}
QPushButton#dangerBtn {
    background-color: transparent;
    border: 1px solid #ef4444;
    color: #ef4444;
}
QLineEdit, QComboBox {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0f172a;
}
QLineEdit:focus {
    border: 1px solid #6366f1;
}
QLabel { color: #0f172a; }
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: transparent;
}
QHeaderView::section {
    background-color: #f1f5f9;
    color: #64748b;
    border: none;
    padding: 10px;
    font-weight: 600;
}
"""

from PyQt5.QtWidgets import QFrame, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor, QPalette

# Premium Deep Space Theme
STYLESHEET = """
/* ================= Global ================= */
QWidget { 
    font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
    color: #f8fafc;
}

QMainWindow, QDialog {
    background-color: #0f172a; /* Rich Slate */
}

/* ================= Buttons ================= */
QPushButton {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #334155, stop:1 #1e293b);
    color: #f8fafc;
    border: 1px solid #475569;
    border-top-color: #64748b; /* Highlight for 3D effect */
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #334155;
    border-color: #94a3b8;
}

QPushButton:pressed {
    background-color: #0f172a;
    border-top-color: #334155;
    padding-top: 11px; /* Press effect */
    padding-bottom: 9px;
}

QPushButton:disabled {
    background-color: #1e293b;
    color: #64748b;
    border-color: #334155;
}

/* Primary Action Button - Indigo Neon Glow */
QPushButton#primaryBtn {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6366f1, stop:1 #4f46e5);
    border: 1px solid #4338ca;
    border-top-color: #818cf8;
    color: #ffffff;
}

QPushButton#primaryBtn:hover {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #818cf8, stop:1 #6366f1);
    border-color: #6366f1;
}

QPushButton#primaryBtn:pressed {
    background-color: #3730a3;
}

/* Danger Button */
QPushButton#dangerBtn {
    background-color: transparent;
    border: 1px solid #ef4444;
    color: #ef4444;
}

QPushButton#dangerBtn:hover {
    background-color: rgba(239, 68, 68, 0.1);
}

/* ================= Sidebar Nav ================= */
QPushButton#navBtn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 8px;
    padding: 12px 16px;
    text-align: left;
    font-weight: 500;
    font-size: 14px;
}

QPushButton#navBtn:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #f1f5f9;
}

QPushButton#navBtn:checked {
    background-color: rgba(99, 102, 241, 0.1);
    color: #818cf8;
    border-left: 3px solid #6366f1;
    border-top-left-radius: 0;
    border-bottom-left-radius: 0;
}

/* ================= Inputs ================= */
QLineEdit, QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 14px;
    color: #f8fafc;
    font-size: 14px;
    selection-background-color: #4f46e5;
}

QLineEdit:hover, QComboBox:hover {
    border-color: #475569;
}

QLineEdit:focus, QComboBox:focus {
    border: 1px solid #6366f1;
    background-color: #0f172a;
}

QLineEdit::placeholder {
    color: #475569;
}

/* ================= Labels ================= */
QLabel {
    color: #f8fafc;
}

QLabel#headerTitle {
    font-size: 24px;
    font-weight: 700;
    color: #f1f5f9;
}

QLabel#subText {
    font-size: 13px;
    color: #94a3b8;
}

QLabel#sectionTitle {
    font-size: 18px;
    font-weight: 600;
    color: #f1f5f9;
    padding-bottom: 8px;
    border-bottom: 1px solid #334155;
    margin-bottom: 8px;
}

/* ================= Tabs ================= */
QTabWidget::pane {
    border: none;
    background: transparent;
}

/* ================= Tables ================= */
QTableWidget {
    background-color: #1e293b;
    alternate-background-color: #0f172a; /* Striped effect */
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: transparent;
    color: #e2e8f0;
}

QTableWidget::item {
    padding: 12px;
    border-bottom: 1px solid #334155;
}

QTableWidget::item:selected {
    background-color: rgba(99, 102, 241, 0.2);
    color: #e0e7ff;
}

QHeaderView::section {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #334155;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
}

/* ================= Progress Protocol ================= */
QProgressBar {
    background-color: #1e293b;
    border-radius: 6px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #818cf8);
    border-radius: 6px;
}

/* ================= Containers ================= */
QFrame#sidebar {
    background-color: #0f172a;
    border-right: 1px solid #334155;
}

QFrame#header {
    background-color: #0f172a;
    border-bottom: 1px solid #334155;
}

QFrame#contentFrame {
    background-color: #0f172a;
}

QFrame#card {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
}

QFrame#statCard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
}

QFrame#statCard:hover {
    border-color: #475569;
    background-color: #252f44;
}

/* ================= Scrollbar ================= */
QScrollBar:vertical {
    background: #0f172a;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* ================= MessageBox ================= */
QMessageBox {
    background-color: #1e293b;
    color: #f1f5f9;
}

QMessageBox QLabel {
    color: #f1f5f9;
}
"""

class StyleHelper:
    @staticmethod
    def set_light_palette(app):
        """Configure global light palette"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(248, 250, 252))
        palette.setColor(QPalette.WindowText, QColor(15, 23, 42))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(248, 250, 252))
        palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        palette.setColor(QPalette.ToolTipText, QColor(15, 23, 42))
        palette.setColor(QPalette.Text, QColor(15, 23, 42))
        palette.setColor(QPalette.Button, QColor(241, 245, 249))
        palette.setColor(QPalette.ButtonText, QColor(15, 23, 42))
        palette.setColor(QPalette.Link, QColor(99, 102, 241))
        palette.setColor(QPalette.Highlight, QColor(99, 102, 241))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        app.setPalette(palette)

    @staticmethod
    def get_header_font(size=16):
        font = QFont("Inter")
        font.setPointSize(size)
        font.setBold(True)
        return font

    @staticmethod
    def get_subheader_font(size=12):
        font = QFont("Inter")
        font.setPointSize(size)
        font.setWeight(QFont.Medium)
        return font

    @staticmethod
    def set_dark_palette(app):
        """Configure global dark palette"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(15, 23, 42))
        palette.setColor(QPalette.WindowText, QColor(248, 250, 252))
        palette.setColor(QPalette.Base, QColor(30, 41, 59))
        palette.setColor(QPalette.AlternateBase, QColor(15, 23, 42))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(248, 250, 252))
        palette.setColor(QPalette.Button, QColor(51, 65, 85))
        palette.setColor(QPalette.ButtonText, QColor(248, 250, 252))
        palette.setColor(QPalette.Link, QColor(99, 102, 241))
        palette.setColor(QPalette.Highlight, QColor(99, 102, 241))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        app.setPalette(palette)

    @staticmethod
    def create_card_frame():
        frame = QFrame()
        frame.setObjectName("card")
        # Add a subtle shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 4)
        frame.setGraphicsEffect(shadow)
        return frame

    @staticmethod
    def create_stat_card():
        frame = QFrame()
        frame.setObjectName("statCard")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        frame.setGraphicsEffect(shadow)
        return frame
