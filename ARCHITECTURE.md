# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌──────────────────────┐          ┌──────────────────────┐     │
│  │  React Web Frontend  │          │  PyQt5 Desktop App   │     │
│  │  (React 18.2.0)      │          │  (Python)            │     │
│  │  - Authentication    │          │  - Authentication    │     │
│  │  - CSV Upload        │          │  - CSV Upload        │     │
│  │  - Charts (Chart.js) │          │  - Charts (Matplotlib)      │
│  │  - History Tracking  │          │  - History Tracking  │     │
│  └──────────────────────┘          └──────────────────────┘     │
│           │ HTTP/HTTPS                       │ HTTP/HTTPS        │
└───────────┼──────────────────────────────────┼──────────────────┘
            │                                  │
┌───────────┴──────────────────────────────────┴──────────────────┐
│                       Network Layer                              │
│                  (CORS, RESTful API)                             │
└──────────────────────────────┬───────────────────────────────────┘
                               │ HTTP/REST
┌──────────────────────────────┴───────────────────────────────────┐
│                         API Layer                                 │
│         Django REST Framework (DRF 3.14.0)                        │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │            Authentication Module                        │    │
│  │  - User Registration                                   │    │
│  │  - Login (Token-based)                                │    │
│  │  - Logout                                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │            Equipment Module                            │    │
│  │  - Upload CSV                                         │    │
│  │  - Parse & Validate Data                             │    │
│  │  - Store in Database                                 │    │
│  │  - Calculate Statistics                              │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │            Analytics Module                            │    │
│  │  - Data Summary API                                   │    │
│  │  - Upload History                                     │    │
│  │  - PDF Generation                                     │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────┬───────────────────────────────────┘
                               │
┌──────────────────────────────┴───────────────────────────────────┐
│                      Business Logic Layer                         │
│                      (Django Models & Signals)                    │
│                                                                   │
│  - Equipment Model                                               │
│  - DataUpload Model                                              │
│  - UserProfile Model                                             │
│  - Signal Handlers                                               │
│  - Data Processing (Pandas)                                      │
│  - PDF Generation (ReportLab)                                    │
└──────────────────────────────┬───────────────────────────────────┘
                               │
┌──────────────────────────────┴───────────────────────────────────┐
│                      Data Layer                                   │
│                     SQLite Database                               │
│                                                                   │
│  Tables:                                                          │
│  - auth_user (User accounts)                                     │
│  - equipment_userprofile                                         │
│  - equipment_equipment (Equipment data)                          │
│  - equipment_dataupload (Upload history)                         │
└───────────────────────────────────────────────────────────────────┘
```

## Component Interaction Flow

### CSV Upload Flow
```
User (Web/Desktop)
    ↓
CSV File Selection
    ↓
Upload API Request
    ↓
Django Backend
    ├─ Validate CSV Format
    ├─ Parse with Pandas
    ├─ Store in Database
    ├─ Calculate Statistics
    └─ Create DataUpload Record
    ↓
Response with Summary
    ↓
Frontend Updates UI
    ├─ Show Success Message
    ├─ Display Charts
    ├─ Update Statistics
    └─ Refresh History
```

### Data Processing Pipeline
```
CSV File Input
    ↓
Pandas Read (CSV Parsing)
    ↓
Data Validation
    ├─ Check Required Columns
    ├─ Validate Data Types
    └─ Sanitize Input
    ↓
Equipment Object Creation
    ├─ Equipment Name
    ├─ Type Classification
    ├─ Numerical Values
    └─ Timestamp
    ↓
Bulk Save to Database
    ↓
Statistics Calculation
    ├─ Total Count
    ├─ Averages (Flowrate, Pressure, Temperature)
    └─ Type Distribution
    ↓
API Response
```

## API Endpoint Structure

```
/api/
├── auth/
│   ├── register/  (POST) - Register new user
│   ├── login/     (POST) - Login user
│   └── logout/    (POST) - Logout user
│
├── equipment/
│   ├── (GET) - List equipment (paginated)
│   ├── {id}/ (GET) - Get equipment detail
│   └── [Detail operations...]
│
├── upload-csv/    (POST) - Upload CSV file
├── summary/       (GET) - Get data summary
├── history/       (GET) - Get upload history
└── generate-pdf/  (POST) - Generate PDF report
```

## Database Schema

### Users (via Django auth)
```sql
User
├── id (Primary Key)
├── username
├── email
├── password_hash
├── first_name
├── last_name
└── created_at
```

### Equipment
```sql
Equipment
├── id (Primary Key)
├── upload_id (Foreign Key → DataUpload)
├── equipment_name
├── equipment_type
├── flowrate (Float)
├── pressure (Float)
├── temperature (Float)
├── created_at (Timestamp)
└── Indexes: [equipment_type], [upload_id]
```

### DataUpload
```sql
DataUpload
├── id (Primary Key)
├── user_id (Foreign Key → User)
├── filename
├── uploaded_at (Timestamp)
├── total_records (Integer)
├── avg_flowrate (Float)
├── avg_pressure (Float)
├── avg_temperature (Float)
└── Indexes: [user_id, uploaded_at]
```

### UserProfile
```sql
UserProfile
├── id (Primary Key)
├── user_id (One-to-One → User)
└── created_at (Timestamp)
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│      Web Server (Nginx/Apache)          │
├─────────────────────────────────────────┤
│   - Serve Static Files                  │
│   - Reverse Proxy to Django             │
│   - HTTPS/SSL                           │
│   - CORS Headers                        │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│   Application Server (Gunicorn/uWSGI)   │
├─────────────────────────────────────────┤
│   - Django Application                  │
│   - Multiple Workers                    │
│   - Load Balancing                      │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│     Database Server (PostgreSQL)        │
├─────────────────────────────────────────┤
│   - Persistent Data Storage             │
│   - Backup & Recovery                   │
│   - Query Optimization                  │
└─────────────────────────────────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│        Authentication Layer             │
│  ├─ Token-based (TokenAuthentication)   │
│  ├─ Session-based                       │
│  └─ CORS Configuration                  │
├─────────────────────────────────────────┤
│        Authorization Layer              │
│  ├─ IsAuthenticated                     │
│  ├─ IsAuthenticatedOrReadOnly           │
│  └─ Custom Permissions                  │
├─────────────────────────────────────────┤
│        Data Validation Layer            │
│  ├─ Serializer Validation               │
│  ├─ Input Sanitization                  │
│  └─ File Upload Validation              │
├─────────────────────────────────────────┤
│        Database Security                │
│  ├─ SQL Injection Prevention            │
│  ├─ Parameterized Queries               │
│  └─ User Data Isolation                 │
└─────────────────────────────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
- Multiple Django instances behind load balancer
- Separate database server
- Redis cache layer
- CDN for static files

### Vertical Scaling
- Database query optimization
- Connection pooling
- Caching strategies
- Async task processing (Celery)

### Performance Optimization
- API pagination
- Database indexing
- Query optimization
- Frontend lazy loading
- Chart.js optimization
