from django.core.management.base import BaseCommand, CommandError
from tender_matching_engine.tender_matching import MatchingTool


class Command(BaseCommand):
    help = 'Performs the process of matching tenders to the keywords they belong to.'

    def handle(self, *args, **options):
        matching_tool = MatchingTool()
        matching_tool.matchTendersToUser()
