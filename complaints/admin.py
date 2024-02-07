# complaints/admin.py
from django.contrib import admin
from .models import Complaint, Category

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'status', 'created_at')

admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Category)
