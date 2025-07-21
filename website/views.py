from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import io

from .models import CustomUser, FormSubmission, CSCAction
from .forms import CustomUserCreationForm, CustomAuthenticationForm, FormSubmissionForm, FormEditForm


def create_superuser_view(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("Superuser created. Please remove this view.")
    return HttpResponse("Superuser already exists.")

def landing_page(request):
    """Landing page with login options"""
    return render(request, 'landing_page.html')

# Authentication Views
def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.user_type == 'user':
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a user account.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form, 'user_type': 'user'})

def csc_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.user_type == 'csc':
                login(request, user)
                return redirect('csc_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a CSC account.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form, 'user_type': 'csc'})

def technician_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.user_type == 'technician':
                login(request, user)
                return redirect('technician_dashboard')
            else:
                messages.error(request, 'Invalid credentials or not a technician account.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form, 'user_type': 'technician'})

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('user_login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing_page')

# Dashboard Views
@login_required
def user_dashboard(request):
    if request.user.user_type != 'user':
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    user_forms = FormSubmission.objects.filter(user=request.user)
    total_forms = user_forms.count()
    completed_forms = user_forms.filter(status='completed').count()
    pending_forms = user_forms.exclude(status='completed').count()
    
    context = {
        'user_forms': user_forms[:5],  # Show latest 5 forms
        'total_forms': total_forms,
        'completed_forms': completed_forms,
        'pending_forms': pending_forms,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def csc_dashboard(request):
    if request.user.user_type != 'csc':
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    pending_forms = FormSubmission.objects.exclude(status__in=['completed']).order_by('-submission_date')
    completed_forms = FormSubmission.objects.filter(status='completed').order_by('-submission_date')
    
    # Pagination
    pending_paginator = Paginator(pending_forms, 10)
    completed_paginator = Paginator(completed_forms, 10)
    
    pending_page = request.GET.get('pending_page')
    completed_page = request.GET.get('completed_page')
    
    pending_forms_page = pending_paginator.get_page(pending_page)
    completed_forms_page = completed_paginator.get_page(completed_page)
    
    context = {
        'pending_forms': pending_forms_page,
        'completed_forms': completed_forms_page,
    }
    return render(request, 'csc/dashboard.html', context)

@login_required
def technician_dashboard(request):
    if request.user.user_type != 'technician':
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    return render(request, 'technician/dashboard.html')

# Form Management Views
@login_required
def create_form(request):
    if request.user.user_type != 'user':
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    if request.method == 'POST':
        form = FormSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form_submission = form.save(commit=False)
            form_submission.user = request.user
            form_submission.save()
            messages.success(request, f'Form #{form_submission.form_id} submitted successfully!')
            return redirect('user_dashboard')
    else:
        form = FormSubmissionForm()
    
    return render(request, 'user/create_form.html', {'form': form, 'show_back_button': True})

@login_required
def view_form(request, form_id):
    form_submission = get_object_or_404(FormSubmission, form_id=form_id)
    
    # Check permissions
    if request.user.user_type == 'user' and form_submission.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('user_dashboard')
    elif request.user.user_type not in ['user', 'csc']:
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    # Log CSC action
    if request.user.user_type == 'csc':
        CSCAction.objects.create(
            form_submission=form_submission,
            csc_user=request.user,
            action_type='viewed'
        )
    
    context = {
        'form_submission': form_submission,
        'show_back_button': True,
    }
    return render(request, 'forms/view_form.html', context)

@login_required
def edit_form(request, form_id):
    if request.user.user_type != 'csc':
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    form_submission = get_object_or_404(FormSubmission, form_id=form_id)
    
    if request.method == 'POST':
        form = FormEditForm(request.POST, instance=form_submission)
        if form.is_valid():
            form.save()
            # Log CSC action
            CSCAction.objects.create(
                form_submission=form_submission,
                csc_user=request.user,
                action_type='edited',
                notes=f"Form updated by {request.user.username}"
            )
            messages.success(request, f'Form #{form_id} updated successfully!')
            return redirect('csc_dashboard')
    else:
        form = FormEditForm(instance=form_submission)
    
    context = {
        'form': form,
        'form_submission': form_submission,
        'show_back_button': True,
    }
    return render(request, 'csc/edit_form.html', context)

@login_required
def submit_form(request, form_id):
    if request.user.user_type != 'csc':
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    form_submission = get_object_or_404(FormSubmission, form_id=form_id)
    form_submission.status = 'completed'
    form_submission.save()
    
    # Log CSC action
    CSCAction.objects.create(
        form_submission=form_submission,
        csc_user=request.user,
        action_type='submitted',
        notes=f"Form completed by {request.user.username}"
    )
    
    messages.success(request, f'Form #{form_id} has been marked as completed!')
    return redirect('csc_dashboard')

@login_required
def user_forms_list(request):
    if request.user.user_type != 'user':
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    user_forms = FormSubmission.objects.filter(user=request.user).order_by('-submission_date')
    
    # Pagination
    paginator = Paginator(user_forms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'forms': page_obj,
        'show_back_button': True,
    }
    return render(request, 'user/forms_list.html', context)

@login_required
def download_form_pdf(request, form_id):
    form_submission = get_object_or_404(FormSubmission, form_id=form_id)
    
    # Check permissions
    if request.user.user_type == 'user' and form_submission.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('user_dashboard')
    elif request.user.user_type not in ['user', 'csc']:
        messages.error(request, 'Access denied.')
        return redirect('landing_page')
    
    # Check if form is completed
    if form_submission.status != 'completed':
        messages.error(request, 'PDF download is only available for completed forms.')
        return redirect('user_dashboard' if request.user.user_type == 'user' else 'csc_dashboard')
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Build PDF content
    story = []
    story.append(Paragraph(f"Form Submission #{form_submission.form_id}", styles['Title']))
    story.append(Spacer(1, 12))
    
    # Form details
    details = [
        f"<b>Full Name:</b> {form_submission.full_name}",
        f"<b>Email:</b> {form_submission.email}",
        f"<b>Phone:</b> {form_submission.phone_number}",
        f"<b>Date of Birth:</b> {form_submission.date_of_birth}",
        f"<b>Occupation:</b> {form_submission.occupation}",
        f"<b>Address:</b> {form_submission.address}",
        f"<b>Purpose:</b> {form_submission.purpose}",
        f"<b>Submission Date:</b> {form_submission.submission_date.strftime('%Y-%m-%d %H:%M:%S')}",
        f"<b>Status:</b> {form_submission.get_status_display()}",
    ]
    
    if form_submission.emergency_contact_name:
        details.append(f"<b>Emergency Contact:</b> {form_submission.emergency_contact_name} - {form_submission.emergency_contact_phone}")
    
    if form_submission.additional_notes:
        details.append(f"<b>Additional Notes:</b> {form_submission.additional_notes}")
    
    if form_submission.comments:
        details.append(f"<b>Comments:</b> {form_submission.comments}")
    
    for detail in details:
        story.append(Paragraph(detail, styles['Normal']))
        story.append(Spacer(1, 6))
    
    doc.build(story)
    buffer.seek(0)
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="form_{form_id}.pdf"'
    
    return response

# Legacy views (keeping for compatibility)
def home(request):
    return redirect('landing_page')

def about(request):
    return HttpResponse("This is the about page")