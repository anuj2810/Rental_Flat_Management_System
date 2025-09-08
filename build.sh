#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Node.js dependencies
npm install

# Build Tailwind CSS
npm run build-css-prod

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate
