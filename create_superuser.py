#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_circle.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@example.com', 
        password='Varun@123',
        role='admin'
    )
    print('Superuser created: admin/Varun@123')
else:
    print('Superuser already exists')