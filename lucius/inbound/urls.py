# inbound/urls.py
from django.urls import path
from . import views_ivr
from . import views_sms

urlpatterns = [
  path('sms', views_sms.sms_response, name='sms'),
  path('answer', views_ivr.answer, name='answer'),
  path('pin_login', views_ivr.pin_login, name='pin_login'),
  
  path('ivr_help', views_ivr.ivr_help, name='ivr_help'),
  path('main_menu', views_ivr.main_menu, name='main_menu'),
  path('main_menu_select', views_ivr.main_menu_select, name='main_menu_select'),
  
  path('start_set_check_interval', views_ivr.start_set_check_interval, name='start_set_check_interval'),
  path('set_check_interval', views_ivr.set_check_interval, name='set_check_interval'),

  path('play_message', views_ivr.play_message, name='play_message'),\
  path('record_message', views_ivr.record_message, name='record_message'),
  path('finish_recording', views_ivr.finish_recording, name='finish_recording'),

  path('list_contacts', views_ivr.list_contacts, name='list_contacts'),
  path('delivery_status', views_ivr.delivery_status, name='delivery_status'),

  path('select_call_contact', views_ivr.select_call_contact, name='select_call_contact'),
  path('make_call', views_ivr.make_call, name='make_call'),
]
