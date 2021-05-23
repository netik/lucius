# inbound/urls.py
from django.urls import path
from . import views_ivr
from . import views_sms

urlpatterns = [
  path('sms', views_sms.sms_response, name='sms'),
  path('answer', views_ivr.answer, name='answer'),
  path('pin_login', views_ivr.pin_login, name='pin_login'),
  path('main_menu', views_ivr.main_menu, name='main_menu'),
  path('main_menu_select', views_ivr.main_menu_select, name='main_menu_select'),
]
