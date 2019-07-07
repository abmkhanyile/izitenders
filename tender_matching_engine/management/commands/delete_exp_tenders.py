from django.core.management.base import BaseCommand, CommandError
from tender_matching_engine.delete_expired_tenders import del_exp_tenders

class Command(BaseCommand):
    help = 'Performs the process of deleting expired tenders from the database.'

    def handle(self, *args, **options):
        del_exp_tenders()