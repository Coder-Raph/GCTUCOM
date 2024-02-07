# complaints/urls.py
from django.urls import path
from .views import solve_complaint  # Fix the import statement here
from . import views

urlpatterns = [
    path('complaint_list/', views.complaint_list, name='complaint_list'),
    path('file_complaint/', views.file_complaint, name='file_complaint'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solve_complaint/<int:complaint_id>/', solve_complaint, name='solve_complaint'),
    # Add more URL patterns as needed
]
