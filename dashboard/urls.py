from django.conf.urls import url, include
from .views import dashboard_view
from tender_details.views import tenders_list_view
from user_accounts.views import profile_view
from .views import tenderList_view, tender_view

urlpatterns = [
    url(r'^$', dashboard_view, name='dashboard'),
    url(r'^matched_tenders_list/(?P<date>\d\d-\d\d-\d\d\d\d)/$', tenderList_view, name='tender_list'),
    url(r'^tender/(?P<tender_pk>\d+)/$', tender_view, name='tender'),
]