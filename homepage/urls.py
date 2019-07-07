from django.urls import path
from django.conf.urls import url
from .views import homeView, province_view


urlpatterns = [
    url(r'^$', homeView, name='homepage'),
]