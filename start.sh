#!/bin/bash

# Quick start script for Flat Rental System (Linux/macOS)
# This script sets up and runs the development server

echo "🚀 Starting Flat Rental System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Run migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Build CSS
echo "🎨 Building CSS..."
npm run build-css-prod

# Check if superuser exists, if not prompt to create one
echo "👤 Checking for admin user..."
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"
if [ $? -ne 0 ]; then
    echo "👤 Creating admin user..."
    echo "Please create an admin account:"
    python manage.py createsuperuser
fi

echo "✅ Setup complete!"
echo "🌐 Starting development server..."
echo ""
echo "Your application will be available at: http://127.0.0.1:8000/"
echo "Press Ctrl+C to stop the server"
echo ""

# Start development server
python manage.py runserver
