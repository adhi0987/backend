from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path('', views.landing_page, name='landing_page'),
    
    # Authentication URLs
    path('user/login/', views.user_login, name='user_login'),
    path('csc/login/', views.csc_login, name='csc_login'),
    path('technician/login/', views.technician_login, name='technician_login'),
    path('user/signup/', views.user_signup, name='user_signup'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard URLs
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('csc/dashboard/', views.csc_dashboard, name='csc_dashboard'),
    path('technician/dashboard/', views.technician_dashboard, name='technician_dashboard'),
    
    # Form management URLs
    path('user/forms/create/', views.create_form, name='create_form'),
    path('user/forms/', views.user_forms_list, name='user_forms_list'),
    path('forms/<int:form_id>/view/', views.view_form, name='view_form'),
    path('forms/<int:form_id>/edit/', views.edit_form, name='edit_form'),
    path('forms/<int:form_id>/submit/', views.submit_form, name='submit_form'),
    path('forms/<int:form_id>/download/', views.download_form_pdf, name='download_form_pdf'),
    
    # Legacy URLs (keeping for compatibility)
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
]