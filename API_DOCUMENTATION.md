# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

### Token Authentication
Include the token in the Authorization header:
```
Authorization: Token <your-token>
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register/`

Request:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response (201):
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "abcdef1234567890",
  "message": "User registered successfully"
}
```

### Login User
**POST** `/auth/login/`

Request:
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

Response (200):
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": "abcdef1234567890",
  "message": "Login successful"
}
```

### Logout User
**POST** `/auth/logout/`

Headers:
```
Authorization: Token <your-token>
```

Response (200):
```json
{
  "message": "Logout successful"
}
```

---

## Equipment Endpoints

### List Equipment
**GET** `/equipment/`

Headers:
```
Authorization: Token <your-token>
```

Query Parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

Response (200):
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/equipment/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "equipment_name": "Pump A1",
      "equipment_type": "pump",
      "flowrate": 100.5,
      "pressure": 10.2,
      "temperature": 25.3,
      "created_at": "2024-01-22T10:30:00Z"
    }
  ]
}
```

### Get Equipment Detail
**GET** `/equipment/{id}/`

Headers:
```
Authorization: Token <your-token>
```

Response (200):
```json
{
  "id": 1,
  "equipment_name": "Pump A1",
  "equipment_type": "pump",
  "flowrate": 100.5,
  "pressure": 10.2,
  "temperature": 25.3,
  "created_at": "2024-01-22T10:30:00Z"
}
```

---

## CSV Upload Endpoint

### Upload CSV File
**POST** `/upload-csv/`

Headers:
```
Authorization: Token <your-token>
Content-Type: multipart/form-data
```

Form Data:
- `file`: CSV file (required)

Example cURL:
```bash
curl -X POST http://localhost:8000/api/upload-csv/ \
  -H "Authorization: Token <your-token>" \
  -F "file=@sample_equipment_data.csv"
```

Response (201):
```json
{
  "id": 1,
  "filename": "sample_equipment_data.csv",
  "uploaded_at": "2024-01-22T10:35:00Z",
  "total_records": 20,
  "avg_flowrate": 85.25,
  "avg_pressure": 11.5,
  "avg_temperature": 45.3,
  "equipment_count": 20
}
```

Error Response (400):
```json
{
  "error": "File must be a CSV file"
}
```

---

## Data Summary Endpoint

### Get Data Summary
**GET** `/summary/`

Headers:
```
Authorization: Token <your-token>
```

Response (200):
```json
{
  "total_count": 50,
  "avg_flowrate": 85.25,
  "avg_pressure": 11.5,
  "avg_temperature": 45.3,
  "equipment_type_distribution": {
    "pump": 10,
    "compressor": 8,
    "reactor": 6,
    "heat_exchanger": 8,
    "separator": 6,
    "mixer": 4,
    "boiler": 4,
    "filter": 4
  },
  "recent_uploads": [
    {
      "id": 1,
      "filename": "sample_equipment_data.csv",
      "uploaded_at": "2024-01-22T10:35:00Z",
      "total_records": 50,
      "avg_flowrate": 85.25,
      "avg_pressure": 11.5,
      "avg_temperature": 45.3,
      "equipment_count": 50
    }
  ]
}
```

Response (200) - No data:
```json
{
  "total_count": 0,
  "avg_flowrate": 0,
  "avg_pressure": 0,
  "avg_temperature": 0,
  "equipment_type_distribution": {},
  "recent_uploads": []
}
```

---

## History Endpoint

### Get Upload History
**GET** `/history/`

Headers:
```
Authorization: Token <your-token>
```

Response (200):
```json
[
  {
    "id": 1,
    "filename": "sample_equipment_data.csv",
    "uploaded_at": "2024-01-22T10:35:00Z",
    "total_records": 50,
    "avg_flowrate": 85.25,
    "avg_pressure": 11.5,
    "avg_temperature": 45.3,
    "equipment_count": 50
  }
]
```

---

## PDF Generation Endpoint

### Generate PDF Report
**POST** `/generate-pdf/`

Headers:
```
Authorization: Token <your-token>
```

Request (Optional):
```json
{
  "upload_id": 1
}
```

Response (200):
- Binary PDF file (Content-Type: application/pdf)
- Content-Disposition: attachment; filename="report_YYYYMMDD.pdf"

Example cURL:
```bash
curl -X POST http://localhost:8000/api/generate-pdf/ \
  -H "Authorization: Token <your-token>" \
  -o report.pdf
```

With specific upload:
```bash
curl -X POST http://localhost:8000/api/generate-pdf/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"upload_id": 1}' \
  -o report.pdf
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Detailed error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Request/Response Examples

### Complete Login and Upload Flow

**1. Register**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**2. Upload CSV**
```bash
curl -X POST http://localhost:8000/api/upload-csv/ \
  -H "Authorization: Token <token_from_register>" \
  -F "file=@sample_equipment_data.csv"
```

**3. Get Summary**
```bash
curl -X GET http://localhost:8000/api/summary/ \
  -H "Authorization: Token <token>"
```

**4. Generate PDF**
```bash
curl -X POST http://localhost:8000/api/generate-pdf/ \
  -H "Authorization: Token <token>" \
  -o report.pdf
```

---

## Rate Limiting

Currently, no rate limiting is applied. For production, consider implementing:
- Token-based throttling
- IP-based throttling
- Endpoint-specific limits

---

## CORS Headers

Allowed Origins:
- `http://localhost:3000` (Web frontend)
- `http://localhost:8000` (Admin)
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8000`

Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS

---

## Testing the API

### Using Postman
1. Create new request
2. Set method and URL
3. Add Authorization header with token
4. Set body (JSON or form data)
5. Send request

### Using cURL
```bash
# Login
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"user","password":"pass"}' | jq -r '.token')

# Use token
curl -X GET http://localhost:8000/api/summary/ \
  -H "Authorization: Token $TOKEN"
```

### Using Python
```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', 
  json={'username': 'user', 'password': 'pass'})
token = response.json()['token']

# Get summary
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://localhost:8000/api/summary/', headers=headers)
print(response.json())
```
