from django.core.management.base import BaseCommand, CommandError
from miscellaneous import script

class Command(BaseCommand):
    help = 'Once off operation.'

    def handle(self, *args, **options):
        script.get_data()