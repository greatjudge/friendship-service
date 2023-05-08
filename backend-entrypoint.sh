#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
# gunicorn friendship.wsgi -b 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000