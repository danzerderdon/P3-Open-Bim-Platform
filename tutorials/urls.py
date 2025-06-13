from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import tutorial_create_landing,create_tutorial, TutorialListView
from django.conf import settings
from django.conf.urls.static import static
from .views import TutorialDetailView




urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('passchange/', views.change_password_view, name='passchange'),
    path('passdone/', views.password_change_done, name='passdone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('change-role/', views.change_role_view, name='change_role'),
    path('tutorials/', TutorialListView.as_view(), name='tutorials'),  # Dummy-URL für Tutorials
    path('create/', views.tutorial_create_landing, name='create'),
    path('files/', views.home, name='files'),     # Dummy-URL für files
    path('community/', views.home, name='community'),     # Dummy-URL für community
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create/new/', create_tutorial, name='tutorial_creator'),
    path('tutorial/<int:tutorial_id>/edit-steps/', views.edit_tutorial_sections, name='edit_tutorial_sections'),
    path('tutorial/<int:tutorial_id>/delete/', views.delete_tutorial, name='delete_tutorial'),
    path('tutorial/<int:tutorial_id>/edit-attributes/', views.edit_tutorial_attributes, name='edit_tutorial_attributes'),
    path('tutorial/<int:tutorial_id>/quiz/', views.edit_tutorial_quiz, name='edit_quiz'),
    path('tutorials/<int:pk>/', views.TutorialDetailView.as_view(), name='tutorial-detail'),
    path('tutorial/<int:tutorial_id>/step/<int:step_order>/',views.tutorial_step,name='tutorial_step'),
    path('tutorial/<int:tutorial_id>/all_steps/',views.tutorial_all_steps,name='tutorial_all_steps'),
    path('tutorial/<int:tutorial_id>/quiz/start/', views.start_quiz, name='start_quiz'),
    path('tutorial/<int:tutorial_id>/quiz/<int:question_order>/', views.quiz_question, name='quiz_question'),
    path('tutorial/<int:tutorial_id>/quiz/result/', views.quiz_result, name='quiz_result'),
    path('tutorials/<int:tutorial_id>/completed_users/', views.completed_users_view, name='completed_users'),
    path('tutorial/<int:tutorial_id>/certificate/print/', views.print_certificate, name='print-certificate'),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

