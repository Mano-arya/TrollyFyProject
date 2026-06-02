# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app

# System deps for psycopg2, Pillow, and common build needs
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     libpq-dev     gcc     curl     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first for better layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip     && pip install --no-cache-dir gunicorn     && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Collect static files at build time
# Make sure your Django settings include:
#   STATIC_ROOT = BASE_DIR / 'staticfiles'
RUN python manage.py collectstatic --noinput

# Cloud Run and many PaaS platforms expect the app to listen on $PORT
ENV PORT=8080

EXPOSE 8080

CMD ["sh", "-c", "gunicorn trollyfy_core.wsgi:application --bind 0.0.0.0:${PORT} --workers 2 --timeout 120"]
