from django.urls import re_path
from .views import dashboard_view
from tender_details.views import tenders_list_view
from user_accounts.views import profile_view, Invoice_view
from .views import tenderList_view, tender_view

urlpatterns = [
    re_path(r'^$', dashboard_view, name='dashboard'),
    re_path(r'^matched_tenders_list/(?P<date>\d\d-\d\d-\d\d\d\d)/$', tenderList_view, name='tender_list'),
    re_path(r'^tender/(?P<tender_pk>\d+)/$', tender_view, name='tender'),
    re_path(r'^invoice/(?P<inv_id>\d+)/$', Invoice_view, name='dashboard_invoice'),
]