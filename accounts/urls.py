from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.signup, name='register'),
    path('adminpage/', views.admin, name='adminpage'),
    path('userpage/', views.user, name='user'),
]