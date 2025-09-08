#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Node.js dependencies
npm install

# Build Tailwind CSS
npm run build-css-prod

# Install Python dependencies
pip install -r requirements.txt

# Create media directories
mkdir -p media/profiles
mkdir -p media/documents/aadhar
mkdir -p media/documents/pan
mkdir -p media/documents/other

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate
