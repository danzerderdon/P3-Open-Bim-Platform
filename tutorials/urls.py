from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('password_change/', views.custom_password_change, name='password_change'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]
