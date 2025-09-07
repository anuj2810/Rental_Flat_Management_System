#!/bin/bash

# Deployment script for Flat Rental System
# Run this script to deploy the application

echo "🚀 Starting deployment of Flat Rental System..."

# Create logs directory if it doesn't exist
mkdir -p logs

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --settings=flat_rental_system.settings_production

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --settings=flat_rental_system.settings_production

# Build CSS
echo "🎨 Building CSS..."
npm run build-css-prod

echo "✅ Deployment completed successfully!"
echo "🌐 You can now start the server with: gunicorn -c gunicorn.conf.py flat_rental_system.wsgi:application"
