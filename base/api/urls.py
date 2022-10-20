from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('events/', views.get_events),
    path('event/<str:pk>/', views.get_event),
]