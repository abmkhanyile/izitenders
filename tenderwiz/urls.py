"""tradeworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from tenderwiz.views import privacy_policy_view, termsAndConditions_view
from homepage.views import province_view

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('homepage.urls')),
    re_path(r'^user_accounts/', include('user_accounts.urls')),
    re_path(r'^about_us/', include('about_us.urls')),
    re_path(r'^contact_us/', include('contact_us.urls')),
    re_path(r'^pricing/', include('pricing.urls')),
    re_path(r'^privacy_policy/$', privacy_policy_view, name='privacy_policy'),
    re_path(r'^province/(?P<province_pk>\d+)/$', province_view, name='province'),
    re_path(r'^termsAndConditions/$', termsAndConditions_view, name='termsAndConditions')
]
