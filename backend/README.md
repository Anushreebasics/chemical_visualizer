# Chemical Equipment Visualizer - Backend

This is the backend server for the Chemical Equipment Visualizer application. It provides a RESTful API for user authentication, CSV data processing, equipment management, and PDF report generation.

## 🚀 Features

- **User Authentication**: Secure Register, Login, and Logout functionality using Django Rest Framework Tokens.
- **CSV Data Processing**: Upload and process chemical equipment data from CSV files using Pandas.
- **Data Analytics**: Automatic calculation of summary statistics (averages, distributions) for uploaded equipment.
- **History Management**: Keeps track of the last 5 data uploads per user.
- **PDF Report Generation**: Generate professional, downloadable PDF reports of equipment data using ReportLab.
- **API Documentation**: Cleanly structured endpoints for frontend integration.

## 🛠 Tech Stack

- **Framework**: [Django 4.2](https://www.djangoproject.com/)
- **API Wrapper**: [Django Rest Framework 3.14](https://www.django-rest-framework.org/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/)
- **PDF Generation**: [ReportLab](https://www.reportlab.com/)
- **Database**: SQLite (Development)
- **Deployment Ready**: Gunicorn & WhiteNoise (for static files)

## 📋 Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)
- `virtualenv` (recommended)

## ⚙️ Installation & Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```
   The backend will be available at `http://127.0.0.1:8000/`.

## 📂 API Reference

| Endpoint | Method | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `/api/auth/register/` | `POST` | Register a new user | No |
| `/api/auth/login/` | `POST` | User login (returns token) | No |
| `/api/auth/logout/` | `POST` | User logout | Yes |
| `/api/upload-csv/` | `POST` | Upload CSV and process equipment data | Yes |
| `/api/summary/` | `GET` | Get overall data statistics and recent uploads | Yes |
| `/api/history/` | `GET` | Get list of last 5 data uploads | Yes |
| `/api/generate-pdf/` | `GET/POST`| Generate PDF report for a specific upload | Yes |
| `/api/equipment/` | `GET/POST`| CRUD operations for equipment items | Yes |

## 📊 CSV Format Requirements

The uploaded CSV should contain the following headers:
- `Equipment Name`
- `Type` (e.g., Pump, Compressor, Reactor, etc.)
- `Flowrate`
- `Pressure`
- `Temperature`

## 🔐 Environment Variables

The application can be configured using environment variables (or a `.env` file):

- `SECRET_KEY`: Django secret key for production.
- `DEBUG`: Set to `True` for development, `False` for production.
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames.
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed frontend origins.

## 📝 Note on Data Retention

To maintain performance, the backend automatically keeps only the **last 5 uploads** per user. Older uploads and their associated equipment data are automatically cleared upon new uploads.
