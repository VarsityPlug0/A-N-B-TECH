from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.conf import settings
import os
import tempfile

from .models import CustomUser, DocumentUpload, Application
from .forms import DocumentUploadForm

class DocumentUploadTestCase(TestCase):
    """
    Test cases for document upload functionality, specifically for 3-month bank statements
    """
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_bank_statement_pdf_upload(self):
        """Test that bank statement PDF uploads work correctly"""
        # Create a mock PDF file
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n'
        pdf_file = SimpleUploadedFile(
            "bank_statement.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        # Test the form validation
        form_data = {'document_type': 'bank_statement'}
        file_data = {'file': pdf_file}
        form = DocumentUploadForm(data=form_data, files=file_data)
        
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
    
    def test_bank_statement_file_size_limit(self):
        """Test that bank statement file size limit is enforced"""
        # Create a file larger than 10MB
        large_content = b'x' * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile(
            "large_bank_statement.pdf",
            large_content,
            content_type="application/pdf"
        )
        
        form_data = {'document_type': 'bank_statement'}
        file_data = {'file': large_file}
        form = DocumentUploadForm(data=form_data, files=file_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('File size must be under 10MB', str(form.errors))
    
    def test_bank_statement_pdf_requirement(self):
        """Test that bank statements must be PDF files"""
        # Try to upload a non-PDF file as bank statement
        jpg_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
        jpg_file = SimpleUploadedFile(
            "bank_statement.jpg",
            jpg_content,
            content_type="image/jpeg"
        )
        
        form_data = {'document_type': 'bank_statement'}
        file_data = {'file': jpg_file}
        form = DocumentUploadForm(data=form_data, files=file_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('Bank statements must be uploaded as PDF files', str(form.errors))
    
    def test_landing_page_bank_statement_upload(self):
        """Test bank statement upload through the landing page"""
        # Create a mock PDF file
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n'
        pdf_file = SimpleUploadedFile(
            "3month_bank_statement.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        # Test the landing page upload
        response = self.client.post(reverse('applications:landing_page'), {
            'document_type': 'bank_statement',
            'file': pdf_file
        })
        
        self.assertEqual(response.status_code, 200)
        # Check that the document was stored in session
        self.assertIn('temp_documents', response.context['request'].session)
    
    def test_bank_statement_filename_validation(self):
        """Test that bank statement filename validation works"""
        # Test with a filename that doesn't suggest it's a bank statement
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n'
        suspicious_file = SimpleUploadedFile(
            "random_document.pdf",
            pdf_content,
            content_type="application/pdf"
        )
        
        form_data = {'document_type': 'bank_statement'}
        file_data = {'file': suspicious_file}
        form = DocumentUploadForm(data=form_data, files=file_data)
        
        # Check if form is valid and print errors if not
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        
        # This should be valid since we're not being too strict with filenames
        # The validation only warns but doesn't fail the form
        self.assertTrue(form.is_valid())
    
    def test_settings_max_upload_size(self):
        """Test that the MAX_UPLOAD_SIZE setting is correctly configured"""
        self.assertEqual(settings.MAX_UPLOAD_SIZE, 10 * 1024 * 1024)  # 10MB
        self.assertIn('pdf', settings.ALLOWED_FILE_EXTENSIONS)
