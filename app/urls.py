__author__ = 'Tadej'
from . import views
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^login/',  views.login, name='login'),
    url(r'^login_action/',  views.login_action, name='login_action'),
    url(r'^index/', views.index, name='index'),
    url(r'^logout_view/', views.logout_view, name='logout'),
    url(r'^import_data/', views.import_data, name='import_data'),
]