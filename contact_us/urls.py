from django.conf.urls import url
from .views import (
    contact_us_view,
    email_success_view,
)

urlpatterns = [
    url(r'^$', contact_us_view, name='contact_us'),
    url(r'^email_sent_success/$', email_success_view, name='email_success'),
]