#!/bin/bash

echo "🧪 Testing Music Web Authentication Flow..."

API_URL="http://localhost:8000/api"

# Test 1: Health check
echo "1️⃣ Testing health endpoint..."
HEALTH=$(curl -s "$API_URL/../health")
if [[ $HEALTH == *"healthy"* ]]; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed: $HEALTH"
    exit 1
fi

# Test 2: Register a new user
echo ""
echo "2️⃣ Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "debuguser",
    "email": "debug@test.com",
    "password": "debug123"
  }')

if [[ $REGISTER_RESPONSE == *"username"* ]]; then
    echo "✅ User registration successful"
    echo "Response: $REGISTER_RESPONSE"
else
    echo "⚠️ Registration response (might be duplicate): $REGISTER_RESPONSE"
fi

# Test 3: Login with the user
echo ""
echo "3️⃣ Testing user login..." 
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "debuguser",
    "password": "debug123"
  }')

if [[ $LOGIN_RESPONSE == *"access_token"* ]]; then
    echo "✅ User login successful"
    TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "Access token: ${TOKEN:0:20}..."
    
    # Test 4: Access protected endpoint
    echo ""
    echo "4️⃣ Testing protected endpoint..."
    ME_RESPONSE=$(curl -s -X GET "$API_URL/auth/me" \
      -H "Authorization: Bearer $TOKEN")
    
    if [[ $ME_RESPONSE == *"username"* ]]; then
        echo "✅ Protected endpoint access successful"
        echo "User info: $ME_RESPONSE"
    else
        echo "❌ Protected endpoint failed: $ME_RESPONSE"
    fi
    
else
    echo "❌ User login failed: $LOGIN_RESPONSE"
fi

echo ""
echo "🏁 Authentication test completed!"