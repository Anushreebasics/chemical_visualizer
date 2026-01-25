# 🖥️ Chemical Equipment Visualizer - Desktop Frontend

A high-performance, asynchronous desktop client for the Chemical Equipment Visualization system. This application provides real-time data analysis, interactive visualizations, and management of equipment datasets via a robust Python architecture.

---

## 🛠️ Technical Stack

*   **Core Logic**: Python 3.8+
*   **UI Framework**: PyQt5 (Qt Widgets & Layouts)
*   **Data Visualization**: Matplotlib (Integrated FigureCanvasQTAgg)
*   **Data Processing**: Pandas (Local validation and serialization)
*   **API Communication**: Requests (RESTful interaction with Django Backend)
*   **Threading**: QThread & Worker patterns for non-blocking I/O

---

## 🏗️ Architecture & Design

### **1. Communication Layer (`api.py`)**
Wraps the `requests` library to handle all backend interactions, including Token Authentication management, Multipart CSV uploads, and Binary data streaming (PDF reports).

### **2. Asynchronous Execution (`workers.py`)**
Critical operations (fetching summaries, heavy CSV uploads) are delegated to background threads using the `QThread` class. This ensures the UI remains responsive (running at 60fps) during heavy network or processing loads.

### **3. Visualization Engine (`charts.py`)**
Custom `MatplotlibCanvas` classes that dynamically render complex data distributions. 
*   **Themes**: Consistent "Dark Slate" aesthetics configured via `rcParams`.
*   **Interactivity**: Integrated `autofmt_xdate` and tight layout management for multi-device support.

### **4. UI Styling (`styles.py`)**
Centralized CSS-like `STYLESHEET` strings applying Global Selectors for consistent padding, border-radius, and typography across all custom QWidgets.

---

## 🚀 Development Setup

### **Environment Initialization**
```bash
# Clone and navigate to the component
cd frontend-desktop

# Create isolated Python environment (USE PYTHON 3.11 or 3.12)
# Note: Python 3.14+ is currently incompatible with pandas C-extensions
python3.12 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### **Execution**
**Standard Launch**:
```bash
python main.py
```

**Developer Launcher (Mac Specific)**:
Automatically configures `PYTHONPATH` and Homebrew links.
```bash
chmod +x run_desktop.sh
./run_desktop.sh
```

---

## 📋 Core Modules Map

| Module | Description |
| :--- | :--- |
| `main_window.py` | Controller for the central layout, navigation tabs, and signal/slot orchestration. |
| `login.py` | UI/Logic for Token acquisition and Session persistence. |
| `charts.py` | Class definitions for Bar, Pie, Doughnut, and Trend Line visualizations. |
| `styles.py` | Theme constants, color palettes, and global QSS definitions. |
| `api.py` | Low-level abstraction for the Django REST Framework API. |

---

## 📦 Features Implementation

*   **Global Search & Filter**: Real-time filtering implemented via `setRowHidden` logic on the Dashboard history table, matching against the local cache of API results.
*   **Adaptive Sorting**: Native Qt item-based sorting enabled for all metrics (Date, Flowrate, Pressure).
*   **PDF Generation**: Direct integration with the backend's ReportLab engine, handled as a background ByteStream download.

---

## ❓ Troubleshooting & Optimization

*   **NameError / Import Errors**: Ensure you are running within the `venv`. The app relies on `QtWidgets.QLineEdit`.
*   **CORS / Connection Refused**: The desktop client expects the backend to be listening at `http://127.0.0.1:8000`. This can be reconfigured in `main_window.py` if needed.
*   **High-DPI Support**: Running on Retina/4K monitors? The framework automatically handles `AA_EnableHighDpiScaling`.
