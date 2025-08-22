#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_circle.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Delete existing admin user if exists
User.objects.filter(username='admin').delete()

# Create new superuser
user = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='Varun@12345',
    role='admin'
)
user.is_staff = True
user.is_superuser = True
user.save()
print('Superuser created: admin/Varun@12345')