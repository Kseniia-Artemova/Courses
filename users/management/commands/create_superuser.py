import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        email = os.getenv('ADMIN_EMAIL')

        if not User.objects.get(email=email).exists():
            superuser = User(
                email=os.getenv('ADMIN_EMAIL'),
                is_active=True,
                is_staff=True,
                is_superuser=True
            )
            superuser.set_password(os.getenv('ADMIN_PASSWORD'))
            superuser.save()
