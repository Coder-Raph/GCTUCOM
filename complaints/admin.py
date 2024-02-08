# complaints/admin.py
from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from .models import Complaint, Category
from .forms import ComplaintForm
from django.urls import path

class ComplaintAdmin(admin.ModelAdmin):
    form = ComplaintForm
    list_display = ('name', 'student_id', 'category', 'description', 'status', 'created_at', 'mark_as_solved_button', 'delete_button')
    search_fields = ('name', 'student_id', 'category__name', 'status')
    list_filter = ('category', 'status', 'created_at')

    def student_id(self, obj):
        return obj.student_id

    student_id.short_description = 'Student ID'

    def mark_as_solved_button(self, obj):
        if obj.status != 'Solved':
            return format_html('<a class="button" href="{}">Mark as Solved</a>', reverse('admin:mark_complaint_as_solved', args=[obj.id]))
        return "-"

    mark_as_solved_button.short_description = 'Mark as Solved'

    def delete_button(self, obj):
        return format_html('<a class="button" href="{}">Delete</a>', reverse('admin:delete_complaint', args=[obj.id]))

    delete_button.short_description = 'Delete'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('mark_solved/<int:complaint_id>/', self.mark_solved, name='mark_complaint_as_solved'),
            path('delete/<int:complaint_id>/', self.delete_complaint, name='delete_complaint'),
        ]
        return custom_urls + urls

    def mark_solved(self, request, complaint_id):
        # Implement the logic to mark the complaint as solved
        complaint = Complaint.objects.get(pk=complaint_id)
        complaint.status = 'Solved'
        complaint.save()
        self.message_user(request, f'Complaint "{complaint}" marked as solved.')
        return HttpResponseRedirect(reverse('admin:complaints_complaint_changelist'))

    def delete_complaint(self, request, complaint_id):
        # Implement the logic to delete the complaint
        complaint = Complaint.objects.get(pk=complaint_id)
        complaint.delete()
        self.message_user(request, f'Complaint "{complaint}" deleted.')
        return HttpResponseRedirect(reverse('admin:complaints_complaint_changelist'))

admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Category)
