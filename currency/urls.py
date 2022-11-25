from django.contrib import admin
from django.urls import path
from currency.views import home, currency, wallet, callback, initiate_payment

urlpatterns = [
   path('', home, name='home'),
   path('currency/', currency, name='currency'),
   path('user-wallet/', wallet, name='wallet'),
   path('pay/', initiate_payment, name='pay'),
   path('callback/', callback, name='callback'),
]
