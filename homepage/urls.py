from django.urls import path, re_path
from .views import homeView, province_view, Testimonial_done_view, Categories_view



urlpatterns = [
    re_path(r'^$', homeView, name='homepage'),
    re_path(r'^testimonial_done/$', Testimonial_done_view, name='Testimonial_done'),
    re_path(r'^tender-categories/$', Categories_view, name='categories')

]