#!/bin/sh
set -e

echo "Starting TrollyFy Django app..."

: "${PORT:=8080}"
: "${DJANGO_SETTINGS_MODULE:=trollyfy_core.settings}"
: "${RUN_MIGRATIONS:=false}"
: "${RUN_COLLECTSTATIC:=false}"
: "${GUNICORN_WORKERS:=2}"
: "${GUNICORN_TIMEOUT:=500}"

export DJANGO_SETTINGS_MODULE

if [ -z "$SECRET_KEY" ]; then
  echo "ERROR: SECRET_KEY environment variable is missing."
  exit 1
fi

if [ -z "$ALLOWED_HOSTS" ]; then
  echo "ERROR: ALLOWED_HOSTS environment variable is missing."
  exit 1
fi

if [ -z "$DB_NAME" ]; then
  echo "ERROR: DB_NAME environment variable is missing."
  exit 1
fi

if [ -z "$DB_USER" ]; then
  echo "ERROR: DB_USER environment variable is missing."
  exit 1
fi

if [ -z "$DB_PASSWORD" ]; then
  echo "ERROR: DB_PASSWORD environment variable is missing."
  exit 1
fi

if [ -z "$DB_HOST" ]; then
  echo "ERROR: DB_HOST environment variable is missing."
  echo "For Cloud SQL Unix socket, use: /cloudsql/PROJECT_ID:REGION:INSTANCE_NAME"
  exit 1
fi

echo "Using Django settings module: ${DJANGO_SETTINGS_MODULE}"
echo "Using Cloud Run port: ${PORT}"
echo "Using database host: ${DB_HOST}"
echo "RUN_COLLECTSTATIC=${RUN_COLLECTSTATIC}"
echo "RUN_MIGRATIONS=${RUN_MIGRATIONS}"

if [ "$RUN_COLLECTSTATIC" = "true" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
else
  echo "Skipping collectstatic."
fi

if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Running database migrations..."
  python manage.py migrate --noinput
else
  echo "Skipping migrations."
fi

echo "Starting Gunicorn on 0.0.0.0:${PORT}..."

exec gunicorn trollyfy_core.wsgi:application \
  --bind 0.0.0.0:${PORT} \
  --workers "${GUNICORN_WORKERS}" \
  --timeout "${GUNICORN_TIMEOUT}" \
  --access-logfile - \
  --error-logfile -
