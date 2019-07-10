from django.urls import path
from django.conf.urls import url
from .views import homeView, province_view, Testimonial_done_view


urlpatterns = [
    url(r'^$', homeView, name='homepage'),
    url(r'^testimonial_done/$', Testimonial_done_view, name='Testimonial_done')
]