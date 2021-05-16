# inbound/urls.py
from django.urls import path

from . import views

urlpatterns = [
  path('answer', views.answer, name='answer'),
  path('login', views.login, name='login'),
  path('main_menu', views.main_menu, name='main_menu'),
  path('main_menu_select', views.main_menu, name='main_menu_select')
]
