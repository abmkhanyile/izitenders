from django.core.management.base import BaseCommand, CommandError
from tender_loader.ethekwini_municipality_scraper import main

class Command(BaseCommand):
    help = 'Scraps tenders from the http://www.durban.gov.za/Resource_Centre/Tenders/Pages/default.aspx site and loads them to the DB.'

    def handle(self, *args, **options):
        main()