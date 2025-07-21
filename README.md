# Form Management System

A comprehensive Django-based form management system with role-based access for Users, CSC (Customer Service Center), and Lab Technicians.

## Features

### Landing Page
- Responsive design with modern UI
- Three login portals: User, CSC, and Lab Technician
- Company information and feature highlights
- Footer with contact information

### User Features
- **User Registration & Login**: Secure authentication system
- **Form Creation**: Comprehensive form with personal information, application details, and document upload
- **Form Tracking**: View all submitted forms with status tracking
- **Status Monitoring**: Real-time status updates (Submitted, Re-submitted, Under Process, Action Needed, Completed)
- **PDF Download**: Download completed forms as PDF documents
- **Dashboard**: Overview of form statistics and recent submissions

### CSC (Customer Service Center) Features
- **Form Management**: View and manage all submitted forms
- **Form Editing**: Edit form details and update status
- **Status Updates**: Change form status and add comments
- **Dual Tables**: Separate tables for pending and completed forms
- **Modal Views**: Quick view of form details in modal windows
- **Action Logging**: Track all CSC actions on forms

### Lab Technician Features
- **Simple Dashboard**: Clean interface for technical staff
- **Future Extensibility**: Framework for adding laboratory-specific features

### Technical Features
- **SQLite Database**: Built-in database for easy deployment
- **File Upload**: Support for document attachments
- **PDF Generation**: Automatic PDF generation for completed forms
- **Responsive Design**: Mobile-friendly interface
- **Admin Panel**: Django admin for system management
- **Pagination**: Efficient handling of large datasets

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd form-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Application: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Default User Accounts

For testing purposes, the following accounts are created:

| Username | Password | User Type | Description |
|----------|----------|-----------|-------------|
| admin | admin123 | Superuser | Admin access |
| testuser | password123 | User | Regular user |
| csc1 | password123 | CSC | CSC staff |
| tech1 | password123 | Technician | Lab technician |

## Application Structure

```
backend/
├── backend/           # Django project settings
├── website/          # Main application
│   ├── models.py     # Database models
│   ├── views.py      # Business logic
│   ├── forms.py      # Django forms
│   ├── urls.py       # URL routing
│   ├── admin.py      # Admin configuration
│   ├── static/       # CSS, JS, images
│   └── templates/    # HTML templates
├── media/            # User uploaded files
├── db.sqlite3        # SQLite database
└── requirements.txt  # Python dependencies
```

## Database Models

### CustomUser
- Extended Django User model
- User types: User, CSC, Lab Technician
- Additional fields: phone_number, user_type

### FormSubmission
- Complete form data storage
- Status tracking with choices
- File upload support
- Timestamps for tracking

### CSCAction
- Audit trail for CSC actions
- Action types: Viewed, Edited, Submitted, Commented
- Linked to forms and CSC users

## API Endpoints

### Authentication
- `/user/login/` - User login
- `/csc/login/` - CSC login
- `/technician/login/` - Technician login
- `/user/signup/` - User registration
- `/logout/` - Logout

### User Dashboard
- `/user/dashboard/` - User dashboard
- `/user/forms/` - User forms list
- `/user/forms/create/` - Create new form

### CSC Dashboard
- `/csc/dashboard/` - CSC dashboard
- `/forms/<id>/edit/` - Edit form
- `/forms/<id>/submit/` - Mark form as completed

### Form Management
- `/forms/<id>/view/` - View form details
- `/forms/<id>/download/` - Download PDF

### Other
- `/` - Landing page
- `/admin/` - Django admin

## Form Fields

The form submission includes:

**Personal Information:**
- Full Name
- Date of Birth
- Email Address
- Phone Number
- Occupation
- Complete Address

**Application Details:**
- Purpose of Application
- Additional Notes
- Previous Applications (checkbox)

**Emergency Contact:**
- Contact Name (optional)
- Contact Phone (optional)

**System Fields:**
- Status tracking
- Comments from CSC
- File attachments
- Timestamps

## Status Flow

1. **Submitted** - Initial status when form is created
2. **Re-submitted** - When form is resubmitted after modifications
3. **Under Process** - CSC is reviewing the form
4. **Action Needed** - User action required
5. **Completed** - Form processing completed, PDF available

## Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

Key responsive features:
- Flexible grid layouts
- Mobile-friendly navigation
- Touch-friendly buttons
- Readable fonts on all devices

## Security Features

- User authentication required for all protected pages
- Role-based access control
- CSRF protection
- Secure file upload handling
- SQL injection protection via Django ORM

## Customization

### Adding New Form Fields
1. Update the `FormSubmission` model in `models.py`
2. Create and run migrations
3. Update forms in `forms.py`
4. Modify templates to include new fields

### Adding New User Types
1. Update `USER_TYPES` in `CustomUser` model
2. Create new dashboard templates
3. Add URL patterns and views
4. Update navigation logic

### Styling Changes
- Modify `website/static/css/style.css`
- Update color schemes, fonts, layouts
- All styles are centralized for easy maintenance

## Production Deployment

For production deployment:

1. **Set DEBUG = False** in settings.py
2. **Configure ALLOWED_HOSTS** with your domain
3. **Use a production database** (PostgreSQL recommended)
4. **Set up static file serving** with whitenoise or web server
5. **Configure email backend** for notifications
6. **Set up HTTPS** for secure communication

## Support

For support or questions:
- Check the Django documentation
- Review the code comments
- Contact the development team

## License

This project is developed for educational and business purposes. Please ensure compliance with your organization's policies before deployment.
