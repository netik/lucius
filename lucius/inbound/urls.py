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
  path('record_message', views_ivr.record_message, name='record_message'),
  path('finish_recording', views_ivr.finish_recording, name='finish_recording'),

]
