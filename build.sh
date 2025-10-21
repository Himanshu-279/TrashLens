#!/usr/bin/env bash
# exit on error
set -o errexit

# Sirf packages install karo aur static files collect karo
pip install -r requirements.txt
python manage.py collectstatic --no-input