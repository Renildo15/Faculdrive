#!/bin/sh

. /opt/venv/bin/activate

python manage.py makemigrations
python manage.py migrate
python manage.py initadmin
python manage.py initgroups
python manage.py initinstitutions

gunicorn buslist.wsgi:application --bind 0.0.0.0:8000