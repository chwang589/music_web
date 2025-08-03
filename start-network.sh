#!/bin/bash

# Music Web Network Deployment Script
echo "🎵 Starting Music Web for network access..."

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the music_web root directory"
    exit 1
fi

# Get local IP address (try multiple methods for reliability)
LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null)

# Fallback IP detection methods
if [ -z "$LOCAL_IP" ] || [ "$LOCAL_IP" = "127.0.0.1" ]; then
    LOCAL_IP=$(ip route get 8.8.8.8 2>/dev/null | awk '{print $7; exit}' 2>/dev/null)
fi

if [ -z "$LOCAL_IP" ] || [ "$LOCAL_IP" = "127.0.0.1" ]; then
    LOCAL_IP=$(ifconfig 2>/dev/null | grep -E "inet.*broadcast" | awk '{print $2}' | head -1)
fi

if [ -z "$LOCAL_IP" ] || [ "$LOCAL_IP" = "127.0.0.1" ]; then
    echo "⚠️  Warning: Could not detect local IP, using localhost"
    LOCAL_IP="localhost"
fi

echo "📡 Local IP detected: $LOCAL_IP"

# Kill existing processes
echo "🔄 Stopping existing servers..."
pkill -f "uvicorn.*app.main:app" 2>/dev/null || true
pkill -f "vite.*dev" 2>/dev/null || true
sleep 2

# Configure frontend for network access with public API
echo "VITE_API_BASE_URL=http://47.97.154.187:9007" > frontend/.env
echo "VITE_HOST=0.0.0.0" >> frontend/.env
echo "VITE_PORT=3000" >> frontend/.env
echo "✅ Frontend configured for network access with public API"

# Start backend with network binding
echo "🚀 Starting backend server on all interfaces..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
for i in {1..15}; do
    if curl -s http://$LOCAL_IP:8000/health > /dev/null 2>&1; then
        echo "✅ Backend server started successfully"
        break
    fi
    if [ $i -eq 15 ]; then
        echo "❌ Backend failed to start after 15 seconds"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    sleep 1
done

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Music Web is now running on the network!"
echo "📱 Access from any device on your network:"
echo "   Frontend: http://$LOCAL_IP:3000"
echo "   Backend API (local): http://$LOCAL_IP:8000"
echo "   Backend API (public): http://47.97.154.187:9007"
echo "   API Docs: http://$LOCAL_IP:8000/docs"
echo ""
echo "🌐 Frontend is configured to use public API endpoint"
echo "📝 To test authentication manually:"
echo "   ./test-auth.sh"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt signal
trap 'echo "🛑 Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT
wait