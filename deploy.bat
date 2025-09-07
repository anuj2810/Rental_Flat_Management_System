@echo off
REM Deployment script for Flat Rental System (Windows)
REM Run this script to deploy the application

echo 🚀 Starting deployment of Flat Rental System...

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Install/update dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Collect static files
echo 📁 Collecting static files...
python manage.py collectstatic --noinput --settings=flat_rental_system.settings_production

REM Run database migrations
echo 🗄️ Running database migrations...
python manage.py migrate --settings=flat_rental_system.settings_production

REM Build CSS
echo 🎨 Building CSS...
npm run build-css-prod

echo ✅ Deployment completed successfully!
echo 🌐 You can now start the server with: gunicorn -c gunicorn.conf.py flat_rental_system.wsgi:application
pause
