from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Crea el objeto Site con ID 1 para que allauth y admin funcionen correctamente'

    def handle(self, *args, **kwargs):
        domain = 'restapitodasxogan.onrender.com'
        name = 'restapitodasxogan'
        site, created = Site.objects.get_or_create(
            id=1, defaults={'domain': domain, 'name': name}
        )
        if not created:
            site.domain = domain
            site.name = name
            site.save()
        self.stdout.write(self.style.SUCCESS(f'Site configurado: {site.domain}'))
