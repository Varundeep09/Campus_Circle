#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_circle.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Promote admin user to superuser
try:
    user = User.objects.get(username='admin')
    user.is_staff = True
    user.is_superuser = True
    user.role = 'admin'  # Change from student to admin
    user.save()
    print(f'User {user.username} promoted to superuser with admin role')
except User.DoesNotExist:
    print('Admin user not found')