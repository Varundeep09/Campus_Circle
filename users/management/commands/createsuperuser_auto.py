from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create superuser automatically'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Varun@123',
                user_type='admin'
            )
            self.stdout.write('Superuser created: admin/Varun@123')
        else:
            self.stdout.write('Superuser already exists')