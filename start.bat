@echo off
REM Quick start script for Flat Rental System (Windows)
REM This script sets up and runs the development server

echo 🚀 Starting Flat Rental System...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies if requirements.txt is newer than last install
echo 📦 Installing/updating dependencies...
pip install -r requirements.txt

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
npm install

REM Run migrations
echo 🗄️ Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Build CSS
echo 🎨 Building CSS...
npm run build-css-prod

REM Check if superuser exists, if not prompt to create one
echo 👤 Checking for admin user...
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)"
if errorlevel 1 (
    echo 👤 Creating admin user...
    echo Please create an admin account:
    python manage.py createsuperuser
)

echo ✅ Setup complete!
echo 🌐 Starting development server...
echo.
echo Your application will be available at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.

REM Start development server
python manage.py runserver
