from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QProgressBar,
    QFrame,
    QScrollArea,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap

from api import APIClient
from charts import MatplotlibCanvas
from styles import STYLESHEET, StyleHelper
from workers import SummaryWorker, UploadWorker


class MainWindow(QMainWindow):
    def __init__(self, token, user):
        super().__init__()
        self.token = token
        self.user = user
        self.client = APIClient(token)
        self.summary_data = None
        self._workers = []  # Track running QThreads

        self.init_ui()
        self.setStyleSheet(STYLESHEET)
        
        # Apply palette for elements not covered by stylesheet
        StyleHelper.set_dark_palette(self)
        
        self.load_all_data()

    # ================= Window =================
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(1200, 760)
        self.resize(1400, 850)
        self.setWindowIcon(self.create_icon())

        root = QWidget()
        root.setObjectName("rootFrame")
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Sidebar on the left
        root_layout.addWidget(self.create_sidebar())
        
        # Main content area on the right
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        
        right_layout.addWidget(self.create_header())
        right_layout.addWidget(self.create_content_frame(), 1)
        
        root_layout.addWidget(right_column, 1)

        self.setCentralWidget(root)
        self.set_active_nav(0)

    def create_icon(self):
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(0, 0, 0, 0)) # Transparent
        return QIcon(pixmap)

    # ================= Sidebar =================
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(260)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(24, 32, 24, 32)
        layout.setSpacing(8)

        # Brand
        brand_layout = QHBoxLayout()
        brand_layout.setSpacing(12)
        
        logo = QLabel("CE")
        logo.setStyleSheet("font-size: 28px;")
        brand_layout.addWidget(logo)
        
        title = QLabel("ChemViz")
        title.setObjectName("headerTitle")
        title.setStyleSheet("font-size: 22px;")
        brand_layout.addWidget(title)
        brand_layout.addStretch()
        
        layout.addLayout(brand_layout)
        layout.addSpacing(40)

        # Navigation
        self.nav_buttons = []
        nav_items = [
            ("Summary", 0, ""),
            ("Charts", 1, ""),
            ("Upload CSV", 2, ""),
            ("History", 3, ""),
        ]

        section_lbl = QLabel("MENU")
        section_lbl.setObjectName("subText")
        section_lbl.setStyleSheet("font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(section_lbl)
        
        for label, idx, icon in nav_items:
            btn = QPushButton(f"{label}")
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, i=idx: self.set_active_nav(i))
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()
        
        # Bottom user info
        user_card = QFrame()
        user_card.setStyleSheet("background-color: #1e293b; border-radius: 12px;")
        uc_layout = QHBoxLayout(user_card)
        uc_layout.setContentsMargins(12, 12, 12, 12)
        
        avatar = QLabel("U")
        avatar.setStyleSheet("background-color: #334155; border-radius: 16px; padding: 6px;")
        
        u_info = QVBoxLayout()
        u_info.setSpacing(2)
        u_name = QLabel(self.user.get('username', 'User'))
        u_name.setStyleSheet("font-weight: 600; color: #f8fafc;")
        u_role = QLabel("Admin")
        u_role.setObjectName("subText")
        u_info.addWidget(u_name)
        u_info.addWidget(u_role)
        
        uc_layout.addWidget(avatar)
        uc_layout.addLayout(u_info)
        uc_layout.addStretch()
        
        layout.addWidget(user_card)
        
        return sidebar

    # ================= Header =================
    def create_header(self):
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(40, 0, 40, 0)
        
        # Breadcrumb or Page Title (Dynamic)
        self.page_title = QLabel("Overview")
        self.page_title.setObjectName("headerTitle")
        self.page_title.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.page_title)
        
        layout.addStretch()

        # Actions
        logout = QPushButton("Logout")
        logout.setObjectName("dangerBtn")
        logout.setCursor(Qt.PointingHandCursor)
        logout.clicked.connect(self.handle_logout)
        layout.addWidget(logout)

        return header

    # ================= Content Area =================
    def create_content_frame(self):
        frame = QFrame()
        frame.setObjectName("contentFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(40, 30, 40, 30)

        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()
        self.tabs.addTab(self.create_summary_tab(), "Summary")
        self.tabs.addTab(self.create_charts_tab(), "Charts")
        self.tabs.addTab(self.create_upload_tab(), "Upload")
        self.tabs.addTab(self.create_history_tab(), "History")

        layout.addWidget(self.tabs)
        return frame

    def set_active_nav(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        self.tabs.setCurrentIndex(index)
        
        titles = ["Overview", "Analytics", "Data Upload", "Upload History"]
        self.page_title.setText(titles[index])

    # ================= Summary Tab =================
    def create_summary_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)

        # Welcome Section
        welcome = QLabel(f"Welcome back, {self.user.get('first_name', self.user.get('username'))}")
        welcome.setStyleSheet("font-size: 16px; color: #94a3b8;")
        layout.addWidget(welcome)

        # Stats Grid
        self.summary_labels = {}
        row = QHBoxLayout()
        row.setSpacing(20)
        
        stats = [
            ("Total Records", "total_count", ""),
            ("Avg Flowrate", "avg_flowrate", ""),
            ("Avg Pressure", "avg_pressure", ""),
            ("Avg Temp", "avg_temperature", ""),
        ]

        for label, key, icon in stats:
            card = StyleHelper.create_stat_card()
            c = QVBoxLayout(card)
            c.setContentsMargins(24, 24, 24, 24)
            c.setSpacing(10)
            
            # Header
            h_layout = QHBoxLayout()
            l = QLabel(label)
            l.setObjectName("subText")
            i = QLabel(icon)
            i.setStyleSheet("font-size: 18px;")
            h_layout.addWidget(l)
            h_layout.addStretch()
            h_layout.addWidget(i)
            c.addLayout(h_layout)
            
            # Value
            v = QLabel("-")
            v.setStyleSheet("font-size: 28px; font-weight: 700; color: #f8fafc;")
            self.summary_labels[key] = v
            c.addWidget(v)
            
            row.addWidget(card)

        layout.addLayout(row)

        # Quick Actions or Recent Activity
        lower_row = QHBoxLayout()
        lower_row.setSpacing(24)
        
        # Chart Preview Card
        chart_card = StyleHelper.create_card_frame()
        cc_layout = QVBoxLayout(chart_card)
        cc_layout.setContentsMargins(24, 24, 24, 24)
        
        cc_title = QLabel("Quick Distribution")
        cc_title.setObjectName("sectionTitle")
        cc_layout.addWidget(cc_title)
        
        self.mini_chart = MatplotlibCanvas(widget, "doughnut")
        self.mini_chart.figure.set_figheight(3)
        cc_layout.addWidget(self.mini_chart)
        
        lower_row.addWidget(chart_card, 2)
        
        # Actions Card
        action_card = StyleHelper.create_card_frame()
        ac_layout = QVBoxLayout(action_card)
        ac_layout.setContentsMargins(24, 24, 24, 24)
        ac_layout.setSpacing(16)
        
        ac_title = QLabel("Actions")
        ac_title.setObjectName("sectionTitle")
        ac_layout.addWidget(ac_title)
        
        pdf_btn = QPushButton("Generate Report")
        pdf_btn.setObjectName("primaryBtn")
        pdf_btn.setFixedHeight(45)
        pdf_btn.setCursor(Qt.PointingHandCursor)
        pdf_btn.clicked.connect(self.generate_pdf)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.setFixedHeight(45)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_all_data)
        
        # New Quick Action
        upload_btn = QPushButton("Upload New File")
        upload_btn.setFixedHeight(45)
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.clicked.connect(lambda: self.set_active_nav(2)) # Navigate to Upload tab
        
        ac_layout.addWidget(pdf_btn)
        ac_layout.addWidget(upload_btn)
        ac_layout.addWidget(refresh_btn)
        ac_layout.addStretch()
        
        lower_row.addWidget(action_card, 1)

        layout.addLayout(lower_row)
        layout.addStretch()
        
        return widget

    # ================= Charts Tab =================
    def create_charts_tab(self):
        widget = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Grid for charts
        from PyQt5.QtWidgets import QGridLayout
        grid = QGridLayout()
        grid.setSpacing(24)
        
        # 1. Trend Line Chart (Full Width or Grid)
        # 2. Pie, 3. Bar, 4. Doughnut
        
        # Creating Canvases
        self.trend_canvas = MatplotlibCanvas(widget, "line")
        self.pie_canvas = MatplotlibCanvas(widget, "pie")
        self.bar_canvas = MatplotlibCanvas(widget, "bar")
        self.doughnut_canvas = MatplotlibCanvas(widget, "doughnut")
        
        # Helper to wrap in card
        def wrap_chart(title, canvas):
            card = StyleHelper.create_card_frame()
            c = QVBoxLayout(card)
            c.setContentsMargins(16, 16, 16, 16)
            
            lbl = QLabel(title)
            lbl.setObjectName("sectionTitle")
            c.addWidget(lbl)
            c.addWidget(canvas)
            return card

        # Layout: 
        # Row 0: Trend (Full Width)
        # Row 1: Pie | Bar
        # Row 2: Doughnut | (Empty or Stats)
        
        # Or 2x2 Grid
        grid.addWidget(wrap_chart("Upload Trends", self.trend_canvas), 0, 0)
        grid.addWidget(wrap_chart("Distribution (Bar)", self.bar_canvas), 0, 1)
        grid.addWidget(wrap_chart("Distribution (Pie)", self.pie_canvas), 1, 0)
        grid.addWidget(wrap_chart("Distribution (Doughnut)", self.doughnut_canvas), 1, 1)
        
        layout.addLayout(grid)
        layout.addStretch()
        
        scroll.setWidget(content)
        
        # Main wrapper
        main_layout = QVBoxLayout(widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
        
        return widget

    # ================= Upload Tab =================
    def create_upload_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignTop)

        card = StyleHelper.create_card_frame()
        card.setFixedWidth(600)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(24)

        icon = QLabel("Upload")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 48px; margin-bottom: 10px;")
        card_layout.addWidget(icon)

        info = QLabel("Select a CSV file to upload equipment data.")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: #94a3b8; font-size: 16px;")
        card_layout.addWidget(info)

        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setAlignment(Qt.AlignCenter)
        self.file_path_label.setStyleSheet("background: #0f172a; padding: 15px; border-radius: 8px; color: #cbd5e1;")
        card_layout.addWidget(self.file_path_label)

        btns = QHBoxLayout()
        btns.setSpacing(16)
        
        browse = QPushButton("Browse Files")
        browse.setCursor(Qt.PointingHandCursor)
        browse.setFixedHeight(45)
        browse.clicked.connect(self.browse_file)

        upload = QPushButton("Upload Data")
        upload.setObjectName("primaryBtn")
        upload.setCursor(Qt.PointingHandCursor)
        upload.setFixedHeight(45)
        upload.clicked.connect(self.upload_file)

        btns.addWidget(browse)
        btns.addWidget(upload)
        card_layout.addLayout(btns)

        self.upload_progress = QProgressBar()
        self.upload_progress.setVisible(False)
        self.upload_progress.setFixedHeight(8)
        card_layout.addWidget(self.upload_progress)

        # Center the card
        container = QHBoxLayout()
        container.addStretch()
        container.addWidget(card)
        container.addStretch()
        
        layout.addSpacing(40)
        layout.addLayout(container)
        return widget

    # ================= History Tab =================
    # ================= History Tab =================
    def create_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # Search Bar
        search_layout = QHBoxLayout()
        search_lbl = QLabel("Search:")
        search_lbl.setStyleSheet("font-size: 16px; color: #94a3b8;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search history by filename...")
        self.search_input.textChanged.connect(self.filter_history)
        
        search_layout.addWidget(search_lbl)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)

        # Table
        self.history_table = QTableWidget(0, 6)
        self.history_table.setHorizontalHeaderLabels(
            ["Filename", "Records", "Flowrate", "Pressure", "Temp", "Action"]
        )
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setShowGrid(False)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSortingEnabled(True) # Enable sorting
        
        # Improve layout behavior
        from PyQt5.QtWidgets import QHeaderView
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch) # Filename takes available space
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.resizeSection(5, 100) # Fixed width for action btn
        
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setFocusPolicy(Qt.NoFocus)

        layout.addWidget(self.history_table)
        return widget

    # ================= Logic =================
    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if path:
            self.file_path = path
            self.file_path_label.setText(path.split('/')[-1])
            self.file_path_label.setStyleSheet("background: #0f172a; padding: 15px; border-radius: 8px; color: #6366f1; border: 1px solid #6366f1;")

    def upload_file(self):
        if not hasattr(self, "file_path"):
            QMessageBox.warning(self, "Error", "Select a CSV file first")
            return

        self.upload_progress.setVisible(True)
        worker = UploadWorker(self.file_path, self.token)
        worker.finished.connect(lambda _: self.load_all_data())
        worker.finished.connect(lambda _: self._cleanup_worker(worker))
        worker.error.connect(lambda _: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def load_all_data(self):
        self.load_summary()
        self.load_chart_data()
        self.load_history()

    def load_summary(self):
        worker = SummaryWorker(self.token)
        worker.finished.connect(self.on_summary_loaded)
        worker.finished.connect(lambda _: self._cleanup_worker(worker))
        worker.error.connect(lambda _: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def load_chart_data(self):
        try:
            response = self.client.get_summary()
            if response.status_code == 200:
                data = response.json()
                dist = data.get("equipment_type_distribution", {})
                uploads = data.get("recent_uploads", [])
                
                # Update Distribution Charts
                if hasattr(self, "bar_canvas"):
                    self.bar_canvas.plot_equipment_distribution(dist)
                if hasattr(self, "pie_canvas"):
                    self.pie_canvas.plot_equipment_distribution(dist)
                if hasattr(self, "doughnut_canvas"):
                    self.doughnut_canvas.plot_equipment_distribution(dist)
                
                # Update Trend Chart
                if hasattr(self, "trend_canvas"):
                    self.trend_canvas.plot_upload_trends(uploads)
                    
                # Mini chart in summary
                if hasattr(self, "mini_chart"):
                    self.mini_chart.plot_equipment_distribution(dist)
        except Exception as e:
            print("Chart data error:", e)

    def load_history(self):
        try:
            response = self.client.get_history()
            if response.status_code == 200:
                data = response.json()
                # Handle pagination (DRF default)
                if isinstance(data, dict) and "results" in data:
                    history = data["results"]
                # Handle custom key
                elif isinstance(data, dict) and "recent_uploads" in data:
                    history = data["recent_uploads"]
                # Handle flat list
                elif isinstance(data, list):
                    history = data
                else:
                    history = []
                
                self.update_history_table(history)
        except Exception as e:
            print("History load error:", e)

    def update_history_table(self, history):
        table = self.history_table
        table.setRowCount(0)
        table.setSortingEnabled(False) # Disable sorting during update
        
        for row, item in enumerate(history):
            table.insertRow(row)
            
            # Helper to create item
            def make_item(text):
                i = QTableWidgetItem(str(text))
                i.setTextAlignment(Qt.AlignCenter)
                return i
                
            table.setItem(row, 0, make_item(item.get("filename", "")))
            table.setItem(row, 1, make_item(item.get("total_records", "")))
            table.setItem(row, 2, make_item(f"{item.get('avg_flowrate', 0):.2f}"))
            table.setItem(row, 3, make_item(f"{item.get('avg_pressure', 0):.2f}"))
            table.setItem(row, 4, make_item(f"{item.get('avg_temperature', 0):.2f}"))
            
            # Action cell
            container = QWidget()
            l = QHBoxLayout(container)
            l.setContentsMargins(4, 4, 4, 4)
            l.setAlignment(Qt.AlignCenter)
            
            # High visibility styling for button
            btn = QPushButton("PDF")
            btn.setFixedSize(60, 30) 
            btn.setCursor(Qt.PointingHandCursor)
            # Use Primary Accent Color (Indigo) for button background, White text
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6366f1; 
                    color: white; 
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #4f46e5;
                }
            """)
            btn.clicked.connect(lambda _, upload_id=item.get("id"): self.generate_pdf(upload_id))
            
            l.addWidget(btn)
            table.setCellWidget(row, 5, container)
            table.setRowHeight(row, 60)
            
        table.setSortingEnabled(True) # Re-enable sorting

    def filter_history(self, text):
        search_text = text.lower()
        for row in range(self.history_table.rowCount()):
            item = self.history_table.item(row, 0) # Filename is column 0
            if not item:
                continue
            
            visible = search_text in item.text().lower()
            self.history_table.setRowHidden(row, not visible)

    def _cleanup_worker(self, worker):
        if worker in self._workers:
            worker.quit()
            worker.wait()
            self._workers.remove(worker)
            if isinstance(worker, UploadWorker):
                self.upload_progress.setVisible(False)
                if hasattr(self, "file_path_label"):
                    self.file_path_label.setText("No file selected")
                    self.file_path_label.setStyleSheet("background: #0f172a; padding: 15px; border-radius: 8px; color: #cbd5e1;")
                delattr(self, "file_path")
                QMessageBox.information(self, "Success", "File uploaded successfully!")

    def closeEvent(self, event):
        for worker in self._workers[:]:
            worker.quit()
            worker.wait()
        self._workers.clear()
        super().closeEvent(event)

    def on_summary_loaded(self, data):
        self.summary_data = data
        for k, lbl in self.summary_labels.items():
            val = data.get(k, 0)
            if isinstance(val, (int, float)):
                val = round(val, 2)
            lbl.setText(str(val))

    def generate_pdf(self, upload_id=None):
        try:
            r = self.client.generate_pdf(upload_id)
            if r.status_code == 200:
                path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "report.pdf", "PDF (*.pdf)")
                if path:
                    with open(path, "wb") as f:
                        f.write(r.content)
                    QMessageBox.information(self, "Success", "PDF Report saved successfully!")
            else:
                 QMessageBox.warning(self, "Error", "Failed to generate PDF")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def handle_logout(self):
        if QMessageBox.question(self, "Logout", "Are you sure you want to logout?") == QMessageBox.Yes:
            self.client.logout()
            self.close()
