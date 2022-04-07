from django.urls import re_path
from .views import (
    contact_us_view,
    email_success_view,
)

urlpatterns = [
    re_path(r'^$', contact_us_view, name='contact_us'),
    re_path(r'^email_sent_success/$', email_success_view, name='email_success'),
]