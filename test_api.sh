#!/bin/bash

# Test Script for Chemical Equipment Visualizer Backend API

BASE_URL="http://localhost:8000"

echo "🧪 Testing Backend API..."
echo "================================"

# Test 1: Register User
echo "\n1. Testing User Registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"TestPass123","email":"test@example.com"}')
  
echo "Response: $REGISTER_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$REGISTER_RESPONSE"

# Extract token
TOKEN=$(echo $REGISTER_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))" 2>/dev/null)

if [ -z "$TOKEN" ]; then
  echo "⚠️  Registration might have failed, trying login..."
  
  # Test 2: Login
  echo "\n2. Testing User Login..."
  LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login/" \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser","password":"TestPass123"}')
    
  echo "Response: $LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LOGIN_RESPONSE"
  
  TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('token', ''))" 2>/dev/null)
fi

if [ -z "$TOKEN" ]; then
  echo "❌ Failed to get authentication token"
  exit 1
fi

echo "✅ Got authentication token: ${TOKEN:0:10}..."

# Test 3: Upload CSV
echo "\n3. Testing CSV Upload..."
CSV_RESPONSE=$(curl -s -X POST "$BASE_URL/api/upload-csv/" \
  -H "Authorization: Token $TOKEN" \
  -F "file=@sample_equipment_data.csv")
  
echo "Response: $CSV_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$CSV_RESPONSE"

# Test 4: Get Data Summary
echo "\n4. Testing Data Summary..."
SUMMARY_RESPONSE=$(curl -s -X GET "$BASE_URL/api/summary/" \
  -H "Authorization: Token $TOKEN")
  
echo "Response: $SUMMARY_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$SUMMARY_RESPONSE"

# Test 5: Get Equipment List
echo "\n5. Testing Equipment List..."
EQUIPMENT_RESPONSE=$(curl -s -X GET "$BASE_URL/api/equipment/" \
  -H "Authorization: Token $TOKEN")
  
echo "Response (first 500 chars): ${EQUIPMENT_RESPONSE:0:500}..."

# Test 6: Get History
echo "\n6. Testing Upload History..."
HISTORY_RESPONSE=$(curl -s -X GET "$BASE_URL/api/history/" \
  -H "Authorization: Token $TOKEN")
  
echo "Response: $HISTORY_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HISTORY_RESPONSE"

echo "\n================================"
echo "✅ All API tests completed!"
