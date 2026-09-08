from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('submit/<int:mov_id>/', views.submit_mov, name='submit_mov'),
]