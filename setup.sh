#!/bin/bash
# Setup script for Chemical Equipment Visualizer

echo "🚀 Setting up Chemical Equipment Visualizer..."

# Backend setup
echo "📦 Setting up backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
echo "✅ Backend setup complete!"

# Frontend Web setup
echo "📦 Setting up web frontend..."
cd ../frontend-web
npm install
echo "✅ Web frontend setup complete!"

# Frontend Desktop setup
echo "📦 Setting up desktop frontend..."
cd ../frontend-desktop
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Desktop frontend setup complete!"

echo ""
echo "🎉 Setup complete! Run the following commands in separate terminals:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend && source venv/bin/activate && python manage.py runserver"
echo ""
echo "Terminal 2 - Web Frontend:"
echo "  cd frontend-web && npm start"
echo ""
echo "Terminal 3 - Desktop App:"
echo "  cd frontend-desktop && source venv/bin/activate && python main.py"
echo ""
