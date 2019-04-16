from django.core.management.base import BaseCommand, CommandError
from tender_loader.etenders_scraper import main

class Command(BaseCommand):
    help = 'Scraps tenders from the eTenders.gov.za site and loads them to the DB.'

    def handle(self, *args, **options):
        main()