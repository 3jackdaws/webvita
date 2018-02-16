#!/usr/bin/env bash



python3 manage.py makemigrations app
python3 manage.py migrate
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin@example.com', 'admin@example.com', 'password')"
gunicorn -b '0.0.0.0:80' --reload app.wsgi


