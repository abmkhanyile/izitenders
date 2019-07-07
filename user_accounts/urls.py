from django.conf.urls import url, include
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
                    )
from tender_details.views import tenders_list_view, send_email_view
from contact_us.views import contact_us_view, email_success_view
from articleApp.views import article_view, article_list_view
from tenderwiz.views import privacy_policy_view, termsAndConditions_view


urlpatterns = [
    url(r'^auth/$', auth_view, name='auth'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^logout_success/$', logout_success_view, name='logout_success'),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^register/(?P<billing_cycle>\d)/(?P<pk>\d+)/$', register_view, name='register'),
    url(r'^tenders/$', tenders_list_view, name='dashboard_tenders'),
    url(r'^articles/$', article_list_view, name='dashboard_article_list'),
    url(r'^article/(?P<article_pk>\d+)/$', article_view, name='article'),
    url(r'^profile/$', profile_view, name='user_profile'),
    url(r'^contact_us/$', contact_us_view, name='dashboard_contact_us'),
    url(r'^invoice/(?P<user_id>\d+)/(?P<comp_prof_id>\d+)/$', Invoice_view, name='invoice'),
    url(r'^registration_success/$', registration_success_view, name='registration_success'),
    url(r'^companyProfileEdit/(?P<pk>\d+)/$', UpdateCompanyProfile, name='company_profile_edit'),
    url(r'^password_change/$', password_change_view, name='password_change'),
    url(r'^password_reset/$', PasswordResetView.as_view(template_name='user_account/password_reset_form.html'), name='password_reset'),
    url(r'^password_reset/done/$', PasswordResetDoneView.as_view(template_name='user_account/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='user_account/password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/done/$', PasswordResetCompleteView.as_view(template_name='user_account/password_reset_complete.html'), name='password_reset_complete'),
    url(r'^auto_complete_search/$', autocomplete_search_view, name='autocomplete_search'),
    url(r'^send_email/$', send_email_view, name='sendEmail'),
    url(r'^payment_success/$', Payment_Success_View, name='payment_success'),
    url(r'^payment_cancelled/$', Payment_Cancelled_View, name='payment_cancelled'),
    url(r'^termsAndConditions/$', termsAndConditions_view, name='dash_ts_and_cs'),
    url(r'^privacy_policy/$', privacy_policy_view, name='dash_privacy_policy'),
    ]