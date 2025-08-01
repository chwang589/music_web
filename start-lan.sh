#!/bin/bash

# Music Web LAN Deployment Script
echo "🎵 Starting Music Web for LAN access..."

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the music_web root directory"
    exit 1
fi

# Get local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "📡 Local IP detected: $LOCAL_IP"

# Check backend dependencies
echo "🔍 Checking backend dependencies..."
cd backend
if ! python -c "import uvicorn" 2>/dev/null; then
    echo "📦 Installing backend dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install backend dependencies"
        exit 1
    fi
fi
cd ..

# Check frontend dependencies
echo "🔍 Checking frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install frontend dependencies"
        exit 1
    fi
fi

# Create frontend .env file with correct API URL
echo "VITE_API_BASE_URL=http://$LOCAL_IP:8000" > .env
echo "✅ Frontend environment configured"
cd ..

# Start backend in background
echo "🚀 Starting backend server..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 2

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend failed to start, stopping backend..."
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Music Web is now running!"
echo "📱 Access from any device on your network:"
echo "   Frontend: http://$LOCAL_IP:3000"
echo "   Backend API: http://$LOCAL_IP:8000"
echo "   API Docs: http://$LOCAL_IP:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt signal
trap 'echo "🛑 Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT
wait