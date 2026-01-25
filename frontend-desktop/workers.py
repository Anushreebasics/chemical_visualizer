from PyQt5.QtCore import QThread, pyqtSignal

from api import APIClient


class UploadWorker(QThread):
    """Worker thread for file upload."""

    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, file_path, token):
        super().__init__()
        self.file_path = file_path
        self.token = token

    def run(self):
        try:
            client = APIClient(self.token)
            response = client.upload_csv(self.file_path)
            if response.status_code == 201:
                self.finished.emit(response.json())
            else:
                self.error.emit(response.json().get('error', 'Upload failed'))
        except Exception as exc:  # pragma: no cover - UI thread boundary
            self.error.emit(str(exc))


class SummaryWorker(QThread):
    """Worker thread for fetching summary."""

    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, token):
        super().__init__()
        self.token = token

    def run(self):
        try:
            client = APIClient(self.token)
            response = client.get_summary()
            if response.status_code == 200:
                self.finished.emit(response.json())
            else:
                self.error.emit('Failed to fetch summary')
        except Exception as exc:  # pragma: no cover - UI thread boundary
            self.error.emit(str(exc))
