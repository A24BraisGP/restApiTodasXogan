# todasXogan/restApi/management/commands/create_admin_user.py
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        admin_nome = 'root' # El nombre de usuario que usarás para el superusuario
        admin_email = 'admin@example.com' # El email del superusuario
        admin_password = 'root123!!' # ¡CAMBIA ESTO POR UNA CONTRASEÑA SEGURA!

        # Usa 'nome' para filtrar, ya que es tu USERNAME_FIELD
        if not User.objects.filter(nome=admin_nome).exists():
            # Crea el superusuario usando 'nome' y 'email'
            User.objects.create_superuser(nome=admin_nome, email=admin_email, password=admin_password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {admin_nome}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {admin_nome} already exists.'))