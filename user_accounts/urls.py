
from django.urls import re_path, path, include
from django.contrib.auth.views import (PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView,
                                       PasswordResetDoneView)
from .views import (login,
                    auth_view,
                    register_view,
                    logout_view,
                    logout_success_view,
                    profile_view,
                    UpdateCompanyProfile,
                    password_change_view,
                    autocomplete_search_view,
                    Invoice_view,
                    registration_success_view,
                    Payment_Success_View,
                    Payment_Cancelled_View,
                    billing_view,
                    )
from tender_details.views import tenders_list_view, send_email_view
from contact_us.views import contact_us_view, email_success_view
from articleApp.views import article_view, article_list_view
from tenderwiz.views import privacy_policy_view, termsAndConditions_view


urlpatterns = [
    re_path(r'^auth/$', auth_view, name='auth'),
    re_path(r'^login/$', login, name='login'),
    re_path(r'^logout/$', logout_view, name='logout'),
    re_path(r'^logout_success/$', logout_success_view, name='logout_success'),
    re_path(r'^dashboard/', include('dashboard.urls')),
    re_path(r'^register/(?P<billing_cycle>\d)/(?P<pk>\d+)/$', register_view, name='register'),
    re_path(r'^tenders/$', tenders_list_view, name='dashboard_tenders'),
    re_path(r'^articles/$', article_list_view, name='dashboard_article_list'),
    re_path(r'^article/(?P<article_pk>\d+)/$', article_view, name='article'),
    re_path(r'^profile/$', profile_view, name='user_profile'),
    re_path(r'^contact_us/$', contact_us_view, name='dashboard_contact_us'),
    re_path(r'^billing/$', billing_view, name='billing'),
    re_path(r'^invoice/(?P<inv_id>\d+)/$', Invoice_view, name='invoice'),
    re_path(r'^registration_success/$', registration_success_view, name='registration_success'),
    re_path(r'^companyProfileEdit/(?P<pk>\d+)/$', UpdateCompanyProfile, name='company_profile_edit'),
    re_path(r'^password_change/$', password_change_view, name='password_change'),
    re_path(r'^password_reset/$', PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    re_path(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    re_path(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    re_path(r'^auto_complete_search/$', autocomplete_search_view, name='autocomplete_search'),
    re_path(r'^send_email/$', send_email_view, name='sendEmail'),
    re_path(r'^payment_success/$', Payment_Success_View, name='payment_success'),
    re_path(r'^payment_cancelled/$', Payment_Cancelled_View, name='payment_cancelled'),
    re_path(r'^termsAndConditions/$', termsAndConditions_view, name='dash_ts_and_cs'),
    re_path(r'^privacy_policy/$', privacy_policy_view, name='dash_privacy_policy'),
    ]