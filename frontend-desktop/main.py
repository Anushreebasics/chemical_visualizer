import sys
from PyQt5.QtWidgets import QApplication, QDialog

from login import LoginDialog
from main_window import MainWindow
from styles import STYLESHEET


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Chemical Equipment Visualizer')
    app.setStyle('Fusion')
    app.setStyleSheet(STYLESHEET)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        window = MainWindow(login_dialog.token, login_dialog.user)
        window.show()
        sys.exit(app.exec_())

    sys.exit()


if __name__ == '__main__':
    main()
