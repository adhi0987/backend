from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Custom User model extending Django's AbstractUser
class CustomUser(AbstractUser):
    USER_TYPES = [
        ('user', 'User'),
        ('csc', 'CSC'),
        ('technician', 'Lab Technician'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='user')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"

# Form submission model
class FormSubmission(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('re-submitted', 'Re-submitted'),
        ('underprocess', 'Under Process'),
        ('action-needed', 'Action Needed'),
        ('completed', 'Completed'),
    ]
    
    # Form identification
    form_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='form_submissions')
    
    # Form fields (based on typical form requirements)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    occupation = models.CharField(max_length=100)
    purpose = models.TextField()
    
    # Additional form fields
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    previous_applications = models.BooleanField(default=False)
    additional_notes = models.TextField(blank=True, null=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submission_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    comments = models.TextField(blank=True, null=True)
    
    # File handling
    document_file = models.FileField(upload_to='form_documents/', blank=True, null=True)
    
    class Meta:
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"Form {self.form_id} - {self.full_name} ({self.status})"

# CSC Actions log
class CSCAction(models.Model):
    ACTION_TYPES = [
        ('viewed', 'Viewed'),
        ('edited', 'Edited'),
        ('submitted', 'Submitted'),
        ('commented', 'Commented'),
    ]
    
    form_submission = models.ForeignKey(FormSubmission, on_delete=models.CASCADE, related_name='csc_actions')
    csc_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'csc'})
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    action_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-action_date']
    
    def __str__(self):
        return f"{self.csc_user.username} {self.action_type} form {self.form_submission.form_id}"
