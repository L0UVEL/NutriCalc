#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

cd nutri_calc
python manage.py collectstatic --no-input
python manage.py migrate --database=mongodb
