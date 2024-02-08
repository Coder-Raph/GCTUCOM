# complaints/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Complaint
from .forms import ComplaintForm
from datetime import datetime

@login_required(login_url='login')
def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.status = 'Unresolved'  # Set initial status to Unresolved
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()

    # Retrieve distinct categories for the filter dropdown
    categories = Category.objects.all()

    return render(request, 'complaints/file_complaint.html', {'form': form, 'categories': categories})

@login_required(login_url='login')
def complaint_list(request):
    # Get filter parameters from the URL
    filter_day = request.GET.get('day')
    filter_month = request.GET.get('month')
    filter_category = request.GET.get('category')

    # Start with all complaints
    complaints = Complaint.objects.all()

    # Apply filters if provided
    if filter_day:
        complaints = complaints.filter(created_at__day=filter_day)
    if filter_month:
        complaints = complaints.filter(created_at__month=filter_month)
    if filter_category:
        complaints = complaints.filter(category__id=filter_category)

    return render(request, 'complaints/complaint_list.html', {'complaints': complaints})

@login_required(login_url='login')
def dashboard(request):
    total_complaints = Complaint.objects.count()
    solved_complaints = Complaint.objects.filter(status='Solved').count()
    unresolved_complaints = Complaint.objects.filter(status='Pending').count()

    # Count complaints per day
    today = datetime.now().date()
    complaints_per_day = Complaint.objects.filter(created_at__date=today).count()

    context = {
        'total_complaints': total_complaints,
        'solved_complaints': solved_complaints,
        'unresolved_complaints': unresolved_complaints,
        'complaints_per_day': complaints_per_day,
    }

    return render(request, 'complaints/dashboard.html', context)

@login_required(login_url='login')
def mark_complaint_as_solved(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    # Add logic to mark the complaint as solved
    complaint.status = 'Solved'
    complaint.save()
    return redirect('complaint_list')  # Redirect to the complaint list after marking as solved

@login_required(login_url='login')
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    # Add logic to delete the complaint
    complaint.delete()
    return redirect('complaint_list')  # Redirect to the complaint list after deletion

def logout_success(request):
    return render(request, 'complaints/logout_success.html')
