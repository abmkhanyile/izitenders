from django.urls import re_path
from .views import pricing_view

urlpatterns = [
    re_path(r'^$', pricing_view, name='pricing'),
]