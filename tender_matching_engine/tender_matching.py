from tender_details.models import Tender, Keywords, Province
from user_accounts.models import CompanyProfile, UsersTenders
from django.utils import timezone
from django.db import transaction


class MatchingTool:
    # This function searches the keywords table in the db if
    # they match the assigned keywordTags to the tenders.
    def matchTendersToUser(self):
        # section below pulls all assigned keywords to the tenders as per the
        # keywordTags field in the tenders db table.
        unmatchedTenders = Tender.objects.all()
        users = CompanyProfile.objects.all()

        for tenderObj in unmatchedTenders:
            tender_provinces = tenderObj.tenderProvince.all()
            tenderKeywords = tenderObj.assigned_keywords.all()

            for user in users:
                userProvinces = user.provinces.all()
                userKeywords = user.keywords.all()

                matchedProvinces = tender_provinces.intersection(userProvinces)
                matchedKeywords = tenderKeywords.intersection(userKeywords)

                if len(matchedProvinces) > 0:
                    if len(matchedKeywords) > 0:
                        with transaction.atomic():
                            if UsersTenders.objects.filter(user=user, tender=tenderObj).exists() == False:
                                UsersTenders.objects.create(user=user, tender=tenderObj)
                                if tenderObj.matched == False:
                                    tenderObj.matched = True
                                    tenderObj.date_assigned = timezone.now()
                                    tenderObj.save()













