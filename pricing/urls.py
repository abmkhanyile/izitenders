from django.conf.urls import url, include
from .views import pricing_view

urlpatterns = [
    url(r'^$', pricing_view, name='pricing'),
    ]