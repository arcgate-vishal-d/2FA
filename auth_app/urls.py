# auth_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('set-two-factor-auth/', views.Set2FAView.as_view()),
]