from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser automatically'

    def handle(self, *args, **options):
        # Delete existing admin user if exists
        User.objects.filter(username='admin').delete()
        
        # Create new superuser
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='Varun@123',
            role='admin'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write('Superuser created: admin/Varun@123')