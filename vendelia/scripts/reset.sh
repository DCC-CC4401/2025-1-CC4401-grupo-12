#!/bin/bash

# Move to project root
cd "$(dirname "$0")/.."

# Test for virtual environment
if [[ -z "$VIRTUAL_ENV" || "$VIRTUAL_ENV" != "$(pwd)/env" ]]; then
    echo "Error: Virtual Environment not active."
    exit 1
fi

# Delete migration files and DB
echo "Deleting migration files and DB"
find marketplace/migrations -type f -name "*.py" ! -name "__init__.py" -delete
find marketplace/migrations -type f -name "*.pyc" -delete
rm -f db.sqlite3

# Run migrations
echo "Running migrations"
python manage.py makemigrations
python manage.py migrate

# Create test superuser if -a flag was passed
if [[ "$1" == "-a" ]]; then
    echo "Creating debug superuser: admin::admin"
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.admin', 'admin')" | python manage.py shell

fi

echo "Operation complete."
