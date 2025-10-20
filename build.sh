#!/usr/bin/env bash
# exit on error
set -o errexit

python manage.py collectstatic --no-input
python manage.py migrate
gunicorn trashlens_project.wsgi --bind 0.0.0.0:7860