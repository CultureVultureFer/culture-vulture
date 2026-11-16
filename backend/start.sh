#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py createsuperuser --noinput || true
exec gunicorn culturevulture.wsgi:application --bind 0.0.0.0:${PORT:-8000}
