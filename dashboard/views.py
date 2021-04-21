from django.shortcuts import render
from user_accounts.models import CompanyProfile
from django.db.models import Count, DateField
from django.db.models.functions import TruncDay
from tender_details.models import Tender
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

#render the dashboard template
@login_required
def dashboard_view(request):
    user = request.user

    companyProfile = CompanyProfile.objects.get(pk=user.id)
    userTenders = companyProfile.assignedTenders.all()
    userTenders = userTenders.distinct()

    tenderSet = userTenders.annotate(d_assigned=TruncDay('date_assigned')).values('d_assigned').annotate(c=Count('id')).values('d_assigned', 'c').order_by("-d_assigned")

    # timedeltas for calculating stats.
    weekly_date = datetime.today() - timedelta(days=7)  # calculates the date from 7 days ago.
    monthly_date = datetime.today() - timedelta(days=30)    # calculates the date from 30 days ago.

    todayStats = userTenders.filter(date_assigned=datetime.today())
    weeklyStats = userTenders.filter(date_assigned__gt=weekly_date)
    monthlyStats = userTenders.filter(date_assigned__gt=monthly_date)

    args = {'user': user,
            'company_profile': companyProfile,
            'tenderSet': tenderSet,
            'totNumOfTenders': userTenders.count(),
            'todayStats': todayStats.count(),
            'weeklyStats': weeklyStats.count(),
            'monthlyStats': monthlyStats.count()
            }
    return render(request, 'dashboard.html', args)


def tenderList_view(request, date):
    companyProfile = CompanyProfile.objects.get(pk=request.user.id)
    user_Tenders = companyProfile.assignedTenders.all()
    user_Tenders = user_Tenders.distinct()

    date = datetime.strptime(date, '%d-%m-%Y')
    tendersPerDate = user_Tenders.filter(date_assigned=date)

    args = {'tenders': tendersPerDate}
    return render(request, 'matched_tenders_list.html', args)

    
@login_required
def tender_view(request, tender_pk):
    tender = Tender.objects.get(pk=tender_pk)
    args = {
        'tender':tender
    }
    return render(request, 'tender.html', args)


