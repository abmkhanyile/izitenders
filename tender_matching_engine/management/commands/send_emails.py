from django.core.management.base import BaseCommand, CommandError
from tender_matching_engine.email_sender import compile_tenders

class Command(BaseCommand):
    help = 'Performs the process of matching tenders to the keywords they belong to...'

    def handle(self, *args, **options):
        compile_tenders()

