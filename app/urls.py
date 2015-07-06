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
    url(r'^settings/schedule/save_simple/', views.save_simple_schedule_settings, name='save_simple_schedule_settings'),
    url(r'^settings/schedule/add_slot/', views.schedule_add_slot, name='schedule_add_slot'),
    url(r'^settings/schedule/add_parallel_slots/', views.schedule_add_parallel_slots, name='schedule_add_parallel_slots'),
    url(r'^settings/schedule/change_slot_length/', views.schedule_change_slot_time, name='schedule_change_slot_length'),
    url(r'^settings/schedule/', views.schedule_settings, name='schedule_settings'),
    url(r'^papers/view/', views.view_paper, name='view_papers'),
    url(r'^papers/update/', views.update_paper, name='update_paper'),
    url(r'^papers/add_to_schedule/', views.add_paper_to_schedule, name='add_paper_to_schedule'),

]