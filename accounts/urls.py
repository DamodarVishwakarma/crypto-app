from django.urls import path
from accounts.views import login_request, register

urlpatterns = [
   path('register/', register, name='register'),
   path('login/', login_request, name='login'),
]
