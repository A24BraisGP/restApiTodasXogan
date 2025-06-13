import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Crea un superusuario desde entorno o valores por defecto si no existe'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'root')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@todasxogan.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123!!')

        if not User.objects.filter(nome=username).exists():
            User.objects.create_superuser(nome=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado.'))
        else:
            self.stdout.write(f'Superusuario "{username}" ya existe.')
