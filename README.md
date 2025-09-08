# 🏠 Flat Rental Management System

A modern, responsive web application for managing rental properties, tenants, and payments. Built with Django and featuring a beautiful, mobile-optimized interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.0+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎯 **Core Functionality**
- **Property Management**: Add, edit, and manage rental flats
- **Tenant Management**: Handle renter accounts and information
- **Rent Tracking**: Monitor monthly rent payments and history
- **Payment Records**: Track payment status and generate reports
- **User Roles**: Separate interfaces for property owners and renters

### 🎨 **Modern Interface**
- **Responsive Design**: Works perfectly on all devices (mobile, tablet, desktop)
- **Dark/Light Theme**: Toggle between themes with smooth transitions
- **Mobile Navigation**: Collapsible menu optimized for mobile devices
- **Beautiful UI**: Modern design with Tailwind CSS and glassmorphism effects
- **Interactive Elements**: Smooth animations and hover effects

### ⚡ **Performance & Security**
- **Optimized Loading**: Fast page loads with optimized CSS (34KB)
- **Security Features**: CSRF protection, XSS prevention, secure headers
- **SEO Ready**: Search engine optimized with proper meta tags
- **Accessibility**: Screen reader friendly with proper focus management

## 🚀 Quick Start

### **Option 1: One-Click Start (Recommended)**

**Windows:**
```bash
# Double-click start.bat or run in terminal:
start.bat
```

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### **Option 2: Manual Setup**

1. **Clone/Download Project**
2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   npm install
   ```
4. **Setup Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. **Build CSS & Start**
   ```bash
   npm run build-css-prod
   python manage.py runserver
   ```

**🌐 Open http://127.0.0.1:8000/ in your browser**

## 📱 Screenshots

### Desktop Interface
- Clean, modern dashboard with statistics
- Intuitive property management interface
- Comprehensive rent tracking system

### Mobile Interface
- Responsive design that works on all screen sizes
- Touch-optimized navigation and buttons
- Compact layouts for mobile devices

## 🛠️ Technology Stack

- **Backend**: Django 5.2.6 (Python)
- **Frontend**: HTML5, Tailwind CSS, Alpine.js
- **Database**: SQLite (development), PostgreSQL (production)
- **Styling**: Tailwind CSS with custom components
- **Icons**: Heroicons (SVG)
- **Deployment**: Gunicorn, Nginx, Docker support

## 📚 Documentation

- **[Complete Setup Guide](DEPLOYMENT.md)** - Detailed installation and deployment instructions
- **[API Documentation](docs/api.md)** - API endpoints and usage (if applicable)
- **[User Guide](docs/user-guide.md)** - How to use the application

## 🔧 Development

### **Development Server**
```bash
python manage.py runserver
```

### **CSS Development**
```bash
# Watch mode for CSS changes
npm run build-css-watch
```

### **Database Operations**
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

## 🚀 Railway Deployment

### **Quick Deploy Steps:**
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Railway"
   git remote add origin https://github.com/YOUR_USERNAME/flat-rental-system.git
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically build and deploy!

3. **Set Environment Variables:**
   ```
   DEBUG=False
   SECRET_KEY=your-super-secret-key-here
   ```

4. **Your app will be live at:** `https://your-app.up.railway.app`

### **One-Click Deploy**
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## 📋 Requirements

- Python 3.8+
- Node.js 16+
- Modern web browser
- 512MB RAM minimum
- 1GB disk space

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed guides
- **Issues**: Create an issue for bug reports or feature requests
- **Email**: Contact support for urgent issues

## 🎉 Acknowledgments

- Django framework for the robust backend
- Tailwind CSS for the beautiful styling
- Alpine.js for interactive components
- All contributors and testers

---

**Made with ❤️ for property management**
