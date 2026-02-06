# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for uploading, processing, and visualizing chemical equipment data. Built with Django backend, React frontend, and PyQt5 desktop application.

## 🌐 Live Demo

- **Web App**: [https://chemical-visualizer-ecru.vercel.app](https://chemical-visualizer-ecru.vercel.app)
- **Backend API**: [https://chemical-equipment-backend-6trw.onrender.com](https://chemical-equipment-backend-6trw.onrender.com)

> ⚠️ **Free-tier cold start notice**: The backend is hosted on Render’s free plan, so it may take **30–60 seconds** to wake up after inactivity. If the app looks stuck:
> 1) Open the Backend API link once to wake the server.
> 2) Wait ~1 minute.
> 3) Refresh the Web App.

## 📋 Project Overview

This application allows users to:
- Upload CSV files containing chemical equipment specifications
- Perform real-time data analysis and visualization
- View equipment type distribution across the inventory
- Generate PDF reports for data analysis
- Access data via both web and desktop interfaces
- Store and manage upload history (last 5 uploads)

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2.7 + Django REST Framework 3.14.0
- **Database**: SQLite
- **Data Processing**: Pandas 2.1.3
- **PDF Generation**: ReportLab 4.0.7
- **Authentication**: Token-based authentication

### Frontend (Web)
- **Framework**: React 18.2.0
- **Routing**: React Router v6
- **HTTP Client**: Axios 1.6.2
- **Charting**: Chart.js 4.4.1
- **Styling**: CSS3

### Frontend (Desktop)
- **Framework**: PyQt5 5.15.9
- **Charting**: Matplotlib 3.8.2
- **Data Processing**: Pandas 2.1.3
- **HTTP Client**: Requests 2.31.0

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                          # Django backend
│   ├── config/                       # Django configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── __init__.py
│   ├── equipment/                    # Equipment app
│   │   ├── models.py                # Equipment, DataUpload, UserProfile models
│   │   ├── views.py                 # API views and business logic
│   │   ├── serializers.py           # DRF serializers
│   │   ├── admin.py                 # Django admin configuration
│   │   ├── apps.py
│   │   ├── signals.py
│   │   └── __init__.py
│   ├── manage.py                     # Django management script
│   ├── db.sqlite3                    # SQLite database
│   └── requirements.txt              # Python dependencies
│
├── frontend-web/                     # React web application
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.js
│   │   │   ├── Register.js
│   │   │   ├── Dashboard.js
│   │   │   └── Auth.css
│   │   │   └── Dashboard.css
│   │   ├── components/
│   │   │   ├── CSVUpload.js
│   │   │   ├── DataSummary.js
│   │   │   ├── Charts.js
│   │   │   ├── History.js
│   │   │   ├── CSVUpload.css
│   │   │   ├── DataSummary.css
│   │   │   ├── Charts.css
│   │   │   └── History.css
│   │   ├── api.js                   # API integration
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── package.json
│   └── README.md
│
├── frontend-desktop/                 # PyQt5 desktop application
│   ├── main.py                       # Main application file
│   ├── requirements.txt              # Python dependencies
│   └── README.md
│
├── sample_equipment_data.csv         # Sample CSV for testing
└── README.md                         # This file
```

## 🚀 Getting Started

> **📝 Note for Deployed App Users**: The live demo is hosted on free-tier services (Render + Vercel). The **first request after inactivity may take 30-60 seconds** as the backend server wakes up. Subsequent requests will be fast. This is normal behavior for free-tier deployments.

### Quick Setup Guide

This project consists of three main components. For detailed setup instructions for each component, please refer to their respective README files:

1. **Backend (Django REST API)** - Required for both frontends
   - See [backend/README.md](backend/README.md) for detailed setup instructions
   - Runs on `http://localhost:8000`

2. **Web Frontend (React)**
   - See [frontend-web/README.md](frontend-web/README.md) for detailed setup instructions
   - Runs on `http://localhost:3000`

3. **Desktop Frontend (PyQt5)**
   - See [frontend-desktop/README.md](frontend-desktop/README.md) for platform-specific setup instructions
   - Standalone desktop application

### Prerequisites
- Python 3.8+ (for backend and desktop app)
- Node.js 14+ (for web frontend)
- Git

### Recommended Setup Order

1. **Start with the Backend** (required)
   ```bash
   cd backend
   # Follow instructions in backend/README.md
   ```

2. **Then choose your frontend:**
   - For web interface: `cd frontend-web` and follow [frontend-web/README.md](frontend-web/README.md)
   - For desktop application: `cd frontend-desktop` and follow [frontend-desktop/README.md](frontend-desktop/README.md)
   - Or set up both for full flexibility!

## 📝 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Equipment Data
- `GET /api/equipment/` - List all equipment (paginated)
- `POST /api/upload-csv/` - Upload and process CSV file
- `GET /api/summary/` - Get data summary and statistics
- `GET /api/history/` - Get upload history (last 5)
- `POST /api/generate-pdf/` - Generate PDF report

## 📊 CSV File Format

The CSV file must contain the following columns:
- **Equipment Name**: String (e.g., "Pump A1")
- **Type**: String (pump, compressor, reactor, heat_exchanger, separator, mixer, boiler, filter, other)
- **Flowrate**: Float (e.g., 100.5)
- **Pressure**: Float (e.g., 10.2)
- **Temperature**: Float (e.g., 25.3)

## 🔐 Features

### Authentication & Security
- Token-based authentication
- User registration and login
- Secure password handling
- CORS enabled for frontend communication

### Data Management
- CSV file upload and validation
- Automatic data parsing and storage
- Equipment type classification
- Last 5 uploads history tracking
- Automatic cleanup of old records

### Analytics & Visualization
- Total equipment count
- Average values calculation (Flowrate, Pressure, Temperature)
- Equipment type distribution
- Interactive charts (Pie, Bar, Doughnut)
- Real-time statistics update

### Reporting
- PDF report generation
- Summary statistics export
- Equipment details export
- Professional formatting

## 🎯 Key Features

1. **Dual Frontend Support**
   - Web-based React application for accessibility
   - Desktop PyQt5 application for offline usage
   - Consistent UI/UX across platforms

2. **Robust Data Processing**
   - CSV validation
   - Data sanitization
   - Error handling
   - Batch processing

3. **Historical Data**
   - Automatic tracking of uploads
   - Last 5 uploads retention
   - Quick PDF generation for past uploads

4. **User Experience**
   - Intuitive interface
   - Real-time data updates
   - Progress indicators
   - Error notifications
   - Responsive design (web)

## 💾 Database Schema

### Equipment Model
```python
- id: Integer (Primary Key)
- upload: ForeignKey to DataUpload
- equipment_name: String
- equipment_type: String (choice field)
- flowrate: Float
- pressure: Float
- temperature: Float
- created_at: DateTime
```

### DataUpload Model
```python
- id: Integer (Primary Key)
- user: ForeignKey to User
- filename: String
- uploaded_at: DateTime
- total_records: Integer
- avg_flowrate: Float
- avg_pressure: Float
- avg_temperature: Float
```

### UserProfile Model
```python
- id: Integer (Primary Key)
- user: OneToOneField to User
- created_at: DateTime
```

## 🧪 Testing

To test the application:

1. Use the sample CSV file: `sample_equipment_data.csv`
2. Register a new user in both web and desktop apps
3. Upload the sample CSV
4. View the generated charts and statistics
5. Generate a PDF report
6. Check the upload history

## 📄 License

This project is created for FOSSEE

## 🔄 Workflow

1. **User Registration**: Create account via login dialog
2. **Upload CSV**: Select and upload CSV file containing equipment data
3. **Data Processing**: Backend validates and processes the CSV
4. **View Analytics**: See charts, statistics, and equipment distribution
5. **Generate Reports**: Export data as PDF for record keeping
6. **Track History**: Access previous uploads and their data

## ⚙️ Configuration

### Backend Configuration (config/settings.py)
- `DEBUG`: Set to False in production
- `ALLOWED_HOSTS`: Add production domain
- `CORS_ALLOWED_ORIGINS`: Update with production URLs
- `SECRET_KEY`: Change in production

### Frontend Configuration (src/api.js)
- `API_BASE_URL`: Update for production deployment
