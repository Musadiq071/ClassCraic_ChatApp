#!/usr/bin/env bash
set -o errexit

# install dependencies
pip install -r requirements.txt

# collect static files
python manage.py collectstatic --no-input

# apply database migrations
python manage.py migrate