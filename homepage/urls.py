from django.urls import path
from django.conf.urls import url
from .views import homeView


urlpatterns = [
    url(r'^$', homeView, name='homepage'),
]