from django.urls import path
from .views import*

urlpatterns = [
    path('signup/admin/',UserSignUpView.as_view(), name='admin_signup'),
    path('signup/user/',AdminUserView.as_view(), name='user_signup'),

   path('login/', LoginView.as_view(), name='login'),
   path('logout/', logout, name='logout'),
]
