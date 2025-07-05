from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
import os

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser
    Adds phone number field for user registration
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.email

def document_upload_path(instance, filename):
    """
    Generate file path for uploaded documents
    Organizes files by user ID and document type
    """
    return f'documents/{instance.user.id}/{instance.document_type}/{filename}'

class DocumentUpload(models.Model):
    """
    Model to store all uploaded documents for iPhone installment applications
    Handles bank statements, payslips, ID pictures, and card images
    """
    DOCUMENT_TYPES = [
        ('bank_statement', 'Bank Statement'),
        ('payslip', 'Payslip'),
        ('id_picture', 'ID Picture'),
        ('card_image', 'Card Image'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(
        upload_to=document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'document_type']
    
    def __str__(self):
        return f"{self.user.email} - {self.get_document_type_display()}"

class Application(models.Model):
    """
    Main application model that ties together user, documents, and phone selection
    Tracks the complete application status and admin approval
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('auto_approved', 'Auto Approved'),
        ('manual_review', 'Manual Review Required'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('manual_payment', 'Manual Payment'),
        ('eft', 'EFT (Electronic Funds Transfer)'),
        ('debit_order', 'Debit Order'),
        ('card_verification', 'Card Verification'),
    ]
    
    PAYMENT_DURATION_CHOICES = [
        (12, '12 Months'),
        (18, '18 Months'),
        (24, '24 Months'),
        (30, '30 Months'),
        (36, '36 Months'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='application')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card_verification')
    payment_duration = models.IntegerField(choices=PAYMENT_DURATION_CHOICES, default=24, help_text='Number of months for installment payment')
    card_number = models.CharField(max_length=19, blank=True, null=True)  # 16 digits + 3 spaces
    card_expiry_month = models.CharField(max_length=2, blank=True, null=True)
    card_expiry_year = models.CharField(max_length=4, blank=True, null=True)
    card_cvv = models.CharField(max_length=4, blank=True, null=True)
    card_last4 = models.CharField(max_length=4, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - Application"
    
    def get_missing_documents(self):
        """
        Check which required documents are missing
        Returns list of missing document types
        """
        required_docs = ['bank_statement', 'id_picture']
        uploaded_docs = [doc.document_type for doc in self.user.documents.all()]
        return [doc for doc in required_docs if doc not in uploaded_docs]
    
    def can_auto_approve(self):
        """
        Check if application can be auto-approved
        Requires bank statement and ID picture
        """
        required_docs = ['bank_statement', 'id_picture']
        uploaded_docs = [doc.document_type for doc in self.user.documents.all()]
        return all(doc in uploaded_docs for doc in required_docs)
    
    def get_total_price(self):
        """
        Calculate total price of all selected phones
        """
        return sum(app_phone.phone.price * app_phone.quantity for app_phone in self.selected_phones.all())
    
    def get_monthly_payment(self):
        """
        Calculate monthly payment amount based on total price and payment duration
        """
        total_price = self.get_total_price()
        # Ensure payment_duration is an integer for comparison
        payment_duration = int(self.payment_duration) if self.payment_duration else 0
        if total_price > 0 and payment_duration > 0:
            return total_price / payment_duration
        return 0
    
    def get_total_interest(self):
        """
        Calculate total interest (assuming 0% for approved applications)
        """
        return 0  # 0% interest for approved applications
    
    def get_total_amount_payable(self):
        """
        Calculate total amount payable including interest
        """
        return self.get_total_price() + self.get_total_interest()
    
    def get_selected_phones_display(self):
        """
        Get a formatted string of all selected phones
        """
        phones = self.selected_phones.all()
        if not phones:
            return "No phones selected"
        return ", ".join([f"{phone.phone.name} {phone.phone.storage} {phone.phone.color}" for phone in phones])
    
    def get_formatted_card_number(self):
        """
        Get formatted card number with asterisks for security
        """
        if self.card_number:
            # Remove spaces and show only last 4 digits
            clean_number = self.card_number.replace(' ', '')
            if len(clean_number) >= 4:
                return f"{'*' * (len(clean_number) - 4)}{clean_number[-4:]}"
        return "Not provided"
    
    def get_formatted_expiry_date(self):
        """
        Get formatted expiry date
        """
        if self.card_expiry_month and self.card_expiry_year:
            return f"{self.card_expiry_month}/{self.card_expiry_year[-2:]}"
        return "Not provided"
    
    def get_full_card_info(self):
        """
        Get complete card information for admin view
        """
        if self.card_number and self.card_expiry_month and self.card_expiry_year and self.card_cvv:
            return {
                'number': self.card_number,
                'expiry': f"{self.card_expiry_month}/{self.card_expiry_year}",
                'cvv': self.card_cvv,
                'last4': self.card_last4 or self.card_number.replace(' ', '')[-4:]
            }
        return None

class ApplicationPhone(models.Model):
    """
    Model to represent phones selected in an application
    Allows multiple phones per application
    """
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='selected_phones')
    phone = models.ForeignKey('Phone', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['application', 'phone']
    
    def __str__(self):
        return f"{self.application.user.email} - {self.phone.name} (x{self.quantity})"
    
    @property
    def total_price(self):
        """
        Calculate total price for this phone selection (price * quantity)
        """
        return self.phone.price * self.quantity

def phone_image_path(instance, filename):
    """
    Generate file path for phone images
    """
    return f'phones/{instance.name}/{filename}'

class Phone(models.Model):
    """
    Model to store available iPhone models and their pricing
    """
    name = models.CharField(max_length=100)  # e.g., "iPhone 13"
    model = models.CharField(max_length=50)  # e.g., "A2482"
    storage = models.CharField(max_length=20)  # e.g., "128GB"
    color = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=phone_image_path, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} {self.storage} {self.color}"
