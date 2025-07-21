from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, FormSubmission, CSCAction

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'email')}),
    )

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('form_id', 'full_name', 'user', 'status', 'submission_date', 'last_updated')
    list_filter = ('status', 'submission_date', 'last_updated', 'previous_applications')
    search_fields = ('full_name', 'email', 'phone_number', 'user__username')
    readonly_fields = ('form_id', 'submission_date', 'last_updated')
    
    fieldsets = (
        ('Form Information', {
            'fields': ('form_id', 'user', 'status', 'submission_date', 'last_updated')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'email', 'phone_number', 'date_of_birth', 'occupation', 'address')
        }),
        ('Application Details', {
            'fields': ('purpose', 'additional_notes', 'previous_applications')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone'),
            'classes': ('collapse',)
        }),
        ('Management', {
            'fields': ('comments', 'document_file')
        }),
    )

@admin.register(CSCAction)
class CSCActionAdmin(admin.ModelAdmin):
    list_display = ('form_submission', 'csc_user', 'action_type', 'action_date')
    list_filter = ('action_type', 'action_date')
    search_fields = ('form_submission__form_id', 'csc_user__username', 'notes')
    readonly_fields = ('action_date',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('form_submission', 'csc_user')
