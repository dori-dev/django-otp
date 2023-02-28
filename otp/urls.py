from django.urls import path
from . import views

urlpatterns = [
    path('', views.phone_login, name='phone_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
