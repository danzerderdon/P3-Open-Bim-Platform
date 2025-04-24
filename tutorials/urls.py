from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import tutorial_create_landing,create_tutorial

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('passchange/', views.change_password_view, name='passchange'),
    path('passdone/', views.password_change_done, name='passdone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('change-role/', views.change_role_view, name='change_role'),
    path('tutorials/', views.home, name='tutorials'),  # Dummy-URL für Tutorials
    path('create/', views.tutorial_create_landing, name='create'),
    path('files/', views.home, name='files'),     # Dummy-URL für files
    path('community/', views.home, name='community'),     # Dummy-URL für community
    path('dashboard/', views.home, name='dashboard'),     # Dummy-URL für dashboard
    path('create/new/', create_tutorial, name='tutorial_creator'),
    path('tutorial/<int:tutorial_id>/edit-steps/', views.edit_tutorial_sections, name='edit_tutorial_sections'),
    path('tutorial/<int:tutorial_id>/delete/', views.delete_tutorial, name='delete_tutorial'),
    path('tutorial/<int:tutorial_id>/edit-attributes/', views.edit_tutorial_attributes, name='edit_tutorial_attributes'),
    path('tutorial/<int:tutorial_id>/quiz/', views.edit_tutorial_quiz, name='edit_quiz'),



]


