from django.conf.urls import url, include
from .views import about_us_view

urlpatterns = [
    url(r'^$', about_us_view, name='about_us'),
]