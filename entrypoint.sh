#!/bin/sh
set -e  # Exit script on error

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting the server..."
exec "$@"
