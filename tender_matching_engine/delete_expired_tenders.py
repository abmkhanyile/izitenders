from tender_details.models import Tender
from django.utils import timezone

def del_exp_tenders():
    expired_tenders = Tender.objects.filter(closingDate__lt=timezone.now())
    if expired_tenders.exists():
        for tender in expired_tenders:
            tender.delete()