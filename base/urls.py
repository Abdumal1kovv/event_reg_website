from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),

    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_page, name='logout'),

    path('user/<str:pk>/', views.user_page, name='profile'),
    path('event/<str:pk>/', views.event_page, name='event'),
    path('register-confirm/<str:pk>/', views.register_confirm, name='register-confirm'),

    path('account/', views.account_page, name='account'),
    path('project-submission/<str:pk>/', views.project_submission, name='project-submission'),

    path('update-submission/<str:pk>/', views.update_submission, name='update-submission'),
]
