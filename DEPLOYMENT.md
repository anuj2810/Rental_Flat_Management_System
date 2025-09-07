# Flat Rental System - Complete Setup & Deployment Guide

## 🚀 **STEP-BY-STEP SETUP FROM SCRATCH**

### **Prerequisites**
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed (optional)

---

## **📋 COMPLETE SETUP PROCESS**

### **Step 1: Download/Clone Project**
```bash
# If using Git:
git clone <your-repo-url>
cd flat_rental_system

# Or download ZIP and extract to flat_rental_system folder
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### **Step 3: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Install Node.js Dependencies**
```bash
npm install
```

### **Step 5: Setup Database**
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts to create admin username, email, and password
```

### **Step 6: Build CSS**
```bash
# Build Tailwind CSS
npm run build-css-prod
```

### **Step 7: Run Development Server**
```bash
# Start development server
python manage.py runserver

# Your application will be available at: http://127.0.0.1:8000/
```

---

## **🌐 PRODUCTION DEPLOYMENT**

### **Method 1: Quick Deployment (Recommended)**

#### **Step 1: Run Deployment Script**
```bash
# On Windows:
deploy.bat

# On macOS/Linux:
chmod +x deploy.sh
./deploy.sh
```

#### **Step 2: Create Environment File**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings:
# - Change SECRET_KEY to a secure random string
# - Set DEBUG=False for production
# - Add your domain to ALLOWED_HOSTS
```

#### **Step 3: Start Production Server**
```bash
# Start with Gunicorn
gunicorn -c gunicorn.conf.py flat_rental_system.wsgi:application

# Your application will be available at: http://0.0.0.0:8000/
```

---

### **Method 2: Manual Deployment**

#### **Step 1: Install Production Dependencies**
```bash
pip install gunicorn python-dotenv whitenoise
```

#### **Step 2: Environment Configuration**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

#### **Step 3: Database & Static Files**
```bash
# Run migrations with production settings
python manage.py migrate --settings=flat_rental_system.settings_production

# Collect static files
python manage.py collectstatic --noinput --settings=flat_rental_system.settings_production

# Build CSS
npm run build-css-prod
```

#### **Step 4: Start Production Server**
```bash
# Start with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 3 flat_rental_system.wsgi:application
```

---

### **Method 3: Docker Deployment (Advanced)**

#### **Step 1: Install Docker**
- Install Docker and Docker Compose on your system

#### **Step 2: Configure Environment**
```bash
# Edit docker-compose.yml and update:
# - SECRET_KEY
# - POSTGRES_PASSWORD
# - ALLOWED_HOSTS
```

#### **Step 3: Deploy with Docker**
```bash
# Build and start all services
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Your application will be available at: http://localhost/
```

---

## **🔧 DEVELOPMENT WORKFLOW**

### **Daily Development**
```bash
# 1. Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# 2. Start development server
python manage.py runserver

# 3. For CSS changes, run in another terminal:
npm run build-css-watch
```

### **Adding New Features**
```bash
# 1. Make model changes
python manage.py makemigrations

# 2. Apply migrations
python manage.py migrate

# 3. Test your changes
python manage.py runserver
```

---

## **🚨 TROUBLESHOOTING**

### **Common Issues & Solutions**

#### **1. CSS Not Loading**
```bash
# Rebuild CSS
npm run build-css-prod
python manage.py collectstatic --noinput
```

#### **2. Database Errors**
```bash
# Reset database (CAUTION: This deletes all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### **3. Permission Errors**
```bash
# On Linux/macOS, fix permissions
chmod +x deploy.sh
sudo chown -R $USER:$USER .
```

#### **4. Port Already in Use**
```bash
# Use different port
python manage.py runserver 8001
# Or kill process using port 8000
```

---

## **📁 PROJECT STRUCTURE**

```
flat_rental_system/
├── accounts/                 # User authentication & profiles
├── flats/                   # Property management
├── rents/                   # Rent tracking
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
├── media/                   # User uploaded files
├── logs/                    # Application logs
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies
├── deploy.sh              # Linux/macOS deployment script
├── deploy.bat             # Windows deployment script
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── gunicorn.conf.py       # Gunicorn configuration
├── nginx.conf             # Nginx configuration
└── .env.example           # Environment variables template
```

---

## **🎯 FEATURES**

### **✅ Complete Features**
- **User Management**: Owner and Renter accounts
- **Property Management**: Add, edit, delete flats
- **Rent Tracking**: Monthly rent records and history
- **Payment Management**: Track payments and dues
- **Responsive Design**: Works on all devices
- **Dark/Light Theme**: Toggle between themes
- **Mobile Navigation**: Collapsible mobile menu
- **Modern UI**: Beautiful Tailwind CSS design
- **Performance Optimized**: Fast loading times
- **SEO Ready**: Search engine optimized

### **🔐 Security Features**
- CSRF protection
- XSS protection
- Secure headers
- Rate limiting
- User authentication
- Permission-based access

---

## **🛠️ MAINTENANCE**

### **Regular Tasks**
1. **Database Backups**: `python manage.py dumpdata > backup.json`
2. **Update Dependencies**: `pip install -r requirements.txt --upgrade`
3. **CSS Updates**: `npm run build-css-prod && python manage.py collectstatic`
4. **Log Monitoring**: Check `logs/` directory for errors

### **Performance Monitoring**
- Monitor server resources (CPU, RAM, disk)
- Check application logs for errors
- Monitor database performance
- Review user feedback

---

## **🚨 SECURITY CHECKLIST**

### **Before Going Live**
- [ ] Change SECRET_KEY to a secure random string
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set up database backups
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerts
- [ ] Review user permissions
- [ ] Test all functionality
- [ ] Set up error logging

---

## **📞 SUPPORT & HELP**

### **Getting Help**
1. Check this documentation first
2. Review error logs in `logs/` directory
3. Check Django documentation: https://docs.djangoproject.com/
4. Check Tailwind CSS documentation: https://tailwindcss.com/docs

### **Common Commands Reference**
```bash
# Development
python manage.py runserver
npm run build-css-watch

# Production
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn -c gunicorn.conf.py flat_rental_system.wsgi:application

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# CSS
npm run build-css-prod
npm run build-css-watch
```

---

## **🎉 CONGRATULATIONS!**

Your Flat Rental System is now ready for deployment!

**🌟 What you have:**
- A complete rental management system
- Beautiful, responsive design
- Mobile-optimized interface
- Production-ready configuration
- Comprehensive documentation

**🚀 Next Steps:**
1. Follow the setup instructions above
2. Customize the system for your needs
3. Deploy to your preferred hosting platform
4. Start managing your rental properties!

**📧 Need Help?** Follow the troubleshooting guide above or review the documentation.
