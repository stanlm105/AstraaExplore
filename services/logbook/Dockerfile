# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Set work directory
WORKDIR /app

RUN useradd -u 10001 -r -s /usr/sbin/nologin appuser && chown -R appuser:appuser /app

# Install system dependencies (if needed for reportlab, e.g., fonts)
RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

USER appuser
# Expose port (match your Flask app, e.g., 5050)
EXPOSE 8080

# Run Gunicorn
CMD exec gunicorn --timeout 120 --bind :$PORT services.logbook.flask_logbook_service:app