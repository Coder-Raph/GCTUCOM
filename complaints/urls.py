# complaints/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('complaint_list/', views.complaint_list, name='complaint_list'),
    path('file_complaint/', views.file_complaint, name='file_complaint'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('mark_solved/<int:complaint_id>/', views.mark_complaint_as_solved, name='mark_complaint_as_solved'),
    path('delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('mark_solved/<int:complaint_id>/', views.mark_complaint_as_solved, name='mark_complaint_as_solved'),
    # Add more URL patterns as needed
]
