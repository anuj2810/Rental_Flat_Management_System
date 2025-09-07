# Dockerfile for Flat Rental System
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=flat_rental_system.settings_production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for CSS building
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and install Node dependencies
COPY package*.json /app/
RUN npm install

# Copy project
COPY . /app/

# Create logs directory
RUN mkdir -p logs

# Build CSS
RUN npm run build-css-prod

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "-c", "gunicorn.conf.py", "flat_rental_system.wsgi:application"]
