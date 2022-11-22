from django.contrib import admin
from django.urls import path
from currency.views import home, currency

urlpatterns = [
   path('', home, name='home'),
   path('currency/', currency, name='currency')
]
