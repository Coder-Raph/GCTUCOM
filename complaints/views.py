from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Complaint
from .forms import ComplaintForm
from datetime import datetime
from django.http import JsonResponse
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType

@login_required(login_url='login')
def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.status = 'Unresolved'
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()

    categories = Category.objects.all()

    return render(request, 'complaints/file_complaint.html', {'form': form, 'categories': categories})

@login_required(login_url='login')
def complaint_list(request):
    filter_day = request.GET.get('day')
    filter_month = request.GET.get('month')
    filter_category = request.GET.get('category')

    complaints = Complaint.objects.all()

    if filter_day:
        complaints = complaints.filter(created_at__day=int(filter_day))
    if filter_month:
        complaints = complaints.filter(created_at__month=int(filter_month))
    if filter_category:
        complaints = complaints.filter(category__name=filter_category)

    return render(request, 'complaints/complaint_list.html', {'complaints': complaints})


@login_required(login_url='login')
def dashboard(request):
    total_complaints = Complaint.objects.count()
    solved_complaints = Complaint.objects.filter(status='Solved').count()
    unresolved_complaints = total_complaints - solved_complaints

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
    if request.method == 'POST' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        complaint_id = request.POST['complaint_id']
        is_checked = request.POST.get('is_checked')

        # Perform necessary actions to mark the complaint as solved based on complaint_id and is_checked
        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status = 'Solved' if is_checked == '1' else 'Unresolved'
        complaint.save()

        # Update the status in the Admin panel
        update_admin_status(complaint, is_checked)

        return JsonResponse({'message': 'Success'}, status=200)

    return JsonResponse({'message': 'Error'}, status=400)

@login_required(login_url='login')
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    # Add logic to delete the complaint
    complaint.delete()
    return redirect('complaint_list')  # Redirect to the complaint list after deletion

def logout_success(request):
    return render(request, 'complaints/logout_success.html')

def update_admin_status(complaint, is_checked):
    # Get the content type for the Complaint model
    content_type = ContentType.objects.get_for_model(complaint)

    # Get the LogEntry for the specific complaint
    log_entry = LogEntry.objects.filter(content_type=content_type, object_id=complaint.id).first()

    if log_entry:
        # Update the action flag based on is_checked
        log_entry.action_flag = CHANGE if is_checked == '1' else 0
        log_entry.save()