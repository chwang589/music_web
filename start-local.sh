#!/bin/bash

# Music Web Local Development Script
echo "🎵 Starting Music Web for local development..."

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the music_web root directory"
    exit 1
fi

# Create frontend .env file for local development
echo "VITE_API_BASE_URL=http://localhost:8000" > frontend/.env
echo "✅ Frontend environment configured for local development"

# Check if backend is already running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend server is already running"
else
    echo "🚀 Starting backend server..."
    cd backend
    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    echo "⏳ Waiting for backend to start..."
    for i in {1..10}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "✅ Backend server started successfully"
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "❌ Backend failed to start"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
fi

# Start frontend if not already running
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend server is already running"
else
    echo "🎨 Starting frontend server..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..
fi

echo ""
echo "🎉 Music Web is now running locally!"
echo "🌐 Access URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop servers"

# Wait for interrupt signal
if [ ! -z "$BACKEND_PID" ] && [ ! -z "$FRONTEND_PID" ]; then
    trap 'echo "🛑 Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT
elif [ ! -z "$FRONTEND_PID" ]; then
    trap 'echo "🛑 Stopping frontend..."; kill $FRONTEND_PID 2>/dev/null; exit 0' INT
fi

wait