from django.core.management.base import BaseCommand, CommandError
from tender_matching_engine.send_mass_emails import send_marketing_emails

class Command(BaseCommand):
    help = 'Performs the process of matching tenders to the keywords they belong to.'

    def handle(self, *args, **options):
        send_marketing_emails()
