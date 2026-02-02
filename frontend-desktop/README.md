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

### **Prerequisites**
- Python 3.8 - 3.12 (Python 3.13+ may have compatibility issues with some dependencies)
- Ensure Python is added to your system PATH

### **Setup Instructions**

#### **For macOS**

**Option 1: Using Homebrew (Recommended)**
```bash
# Navigate to the desktop frontend
cd frontend-desktop

# Install Python 3.11 via Homebrew
brew install python@3.11

# Install PyQt5 via Homebrew (provides better macOS integration)
brew install pyqt@5

# Install other Python dependencies
/opt/homebrew/bin/pip3 install -r requirements.txt

# Make the launcher executable and run
chmod +x run_desktop.sh
./run_desktop.sh
```

**Option 2: Using Virtual Environment**
```bash
cd frontend-desktop

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### **For Windows**

```powershell
# Navigate to the desktop frontend
cd frontend-desktop

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### **For Linux**

```bash
cd frontend-desktop

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-pyqt5 python3-pip

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
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

*   **CORS / Connection Refused**: The desktop client expects the backend to be listening at `http://127.0.0.1:8000`. This can be reconfigured in `main_window.py` if needed.
*   **High-DPI Support**: Running on Retina/4K monitors? The framework automatically handles `AA_EnableHighDpiScaling`.
