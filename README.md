# iPhone Installment Store

A comprehensive Django web application for managing iPhone installment purchases with document verification, user registration, and admin approval workflows.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/iphone-store.git
cd iphone-store

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate sample data
python manage.py populate_phones

# Run development server
python manage.py runserver
```

Visit http://localhost:8000/applications/ to start using the application!

## Features

### User Features
- **Document Upload System**: Upload bank statements, payslips, ID pictures, and card images
- **Auto-Verification**: Automatic approval when required documents are present
- **User Registration**: Complete account creation with personal information
- **iPhone Selection**: Choose from various iPhone models with pricing
- **Payment Verification**: Secure card information collection
- **Application Dashboard**: Track application status and progress
- **Email Notifications**: Automatic email alerts to admins

### Admin Features
- **Application Management**: Review and approve/reject applications
- **Document Review**: View uploaded documents with secure access
- **Status Tracking**: Monitor application progress and status
- **Bulk Actions**: Approve or reject multiple applications
- **Admin Dashboard**: Comprehensive admin interface
- **Email Integration**: Receive application notifications with attachments

### Security Features
- **File Validation**: Secure file upload with size and type restrictions
- **Document Encryption**: Secure storage of sensitive documents
- **PCI Compliance**: Card information handled securely
- **Session Management**: Secure user sessions
- **Input Sanitization**: All user inputs validated and sanitized

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (can be configured for PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5.3.0, Font Awesome 6.0.0
- **File Storage**: Django's built-in file storage system
- **Email**: Django's email backend (configurable for SMTP)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation

### Option 1: Quick Start (Recommended)
Follow the quick start guide above for the fastest setup.

### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/iphone-store.git
   cd iphone-store
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data**
   ```bash
   python manage.py populate_phones
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://localhost:8000/applications/
   - Admin panel: http://localhost:8000/admin/

## Application Flow

### Step 1: Document Upload (Landing Page)
- Users upload required documents:
  - **Bank Statement** (Required)
  - **ID Picture** (Required)
  - **Payslip** (Optional but recommended)
- System validates file types and sizes
- Auto-verification when required documents are present

### Step 2: User Registration
- Collect personal information:
  - Full name
  - Email address
  - Phone number
  - Username and password
- Create user account and application record
- Process uploaded documents

### Step 3: iPhone Selection
- Display available iPhone models with pricing
- User selects preferred model and configuration
- Update application with selection

### Step 4: Payment Information
- Upload card image (for verification)
- Enter last 4 digits of card number
- Complete application submission

### Step 5: Admin Review
- Admin receives email notification with attachments
- Review application in admin panel
- Approve, reject, or flag for manual review
- Update application status

## Models

### CustomUser
- Extends Django's AbstractUser
- Adds phone_number field
- Used for user authentication and personal information

### DocumentUpload
- Stores uploaded documents (bank statements, payslips, IDs, card images)
- File validation and secure storage
- Organized by user and document type

### Application
- Main application model linking user, documents, and phone selection
- Tracks verification status and admin approval
- Status options: pending, auto_approved, manual_review, approved, rejected

### Phone
- Stores available iPhone models and configurations
- Includes pricing and availability status
- Supports multiple storage options and colors

## Admin Interface

### Application Management
- View all applications with filtering and search
- Review uploaded documents
- Update application status
- Bulk approve/reject actions

### Document Review
- Secure access to uploaded files
- Document type categorization
- Upload date tracking

### User Management
- View user information and applications
- Manage user permissions
- Track user activity

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root for sensitive configuration:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/iphone_store

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# File Storage (for production)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```

### Email Configuration
The application sends email notifications to admins when applications are submitted. Configure email settings in `settings.py`:

```python
# For development (console output)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# For production (SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## Security Features

### File Upload Security
- File type validation (PDF, JPG, JPEG, PNG)
- File size limits (5MB maximum)
- Secure file storage with organized directory structure
- File content validation

### Data Protection
- All sensitive data encrypted
- Card information limited to last 4 digits
- Secure session management
- Input sanitization and validation

### Access Control
- Admin-only access to sensitive functions
- User authentication required for application flow
- Secure document access controls

## Customization

### Adding New iPhone Models
Use the admin interface or create a new management command:

```python
from applications.models import Phone

Phone.objects.create(
    name='iPhone 16',
    model='A4000',
    storage='128GB',
    color='Space Black',
    price=899.00,
    is_available=True
)
```

### Modifying Document Requirements
Update the `get_missing_documents()` method in the Application model:

```python
def get_missing_documents(self):
    required_docs = ['bank_statement', 'id_picture', 'new_document']
    uploaded_docs = [doc.document_type for doc in self.user.documents.all()]
    return [doc for doc in required_docs if doc not in uploaded_docs]
```

### Custom Email Templates
Modify the `send_application_email()` function in `views.py` to customize email content and formatting.

## Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure a production database (PostgreSQL recommended)
3. Set up proper email backend
4. Configure static file serving
5. Set secure `SECRET_KEY`
6. Configure `ALLOWED_HOSTS`

### File Storage
For production, consider using cloud storage services:
- AWS S3
- Google Cloud Storage
- Azure Blob Storage

### Security Checklist
- [ ] Use HTTPS in production
- [ ] Configure proper CORS settings
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Regular security updates

## 🧪 Testing

### Running Tests
```bash
python manage.py test
```

### Running with Sample Data
```bash
# Add test card data
python manage.py add_test_card_data

# Populate with sample phones
python manage.py populate_phones
```

## 🚀 Deployment

### Heroku Deployment
1. Install Heroku CLI
2. Create a new Heroku app
3. Add PostgreSQL addon
4. Configure environment variables
5. Deploy:
   ```bash
   git push heroku main
   ```

### Docker Deployment
```bash
# Build the image
docker build -t iphone-store .

# Run the container
docker run -p 8000:8000 iphone-store
```

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up proper email backend
- [ ] Configure static file serving
- [ ] Set secure `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up SSL/HTTPS
- [ ] Configure logging
- [ ] Set up monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings to new functions
- Write tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@iphonestore.com
- Documentation: [Link to documentation]
- Issues: [GitHub issues page]

## Changelog

### Version 1.0.0
- Initial release
- Complete application flow
- Admin interface
- Email notifications
- Security features
- Document management 