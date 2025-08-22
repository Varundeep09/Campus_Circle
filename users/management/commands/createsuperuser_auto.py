from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser automatically'

    def handle(self, *args, **options):
        # Promote admin user to superuser
        try:
            user = User.objects.get(username='admin')
            user.is_staff = True
            user.is_superuser = True
            user.role = 'admin'  # Change from student to admin
            user.save()
            self.stdout.write(f'User {user.username} promoted to superuser with admin role')
        except User.DoesNotExist:
            self.stdout.write('Admin user not found')