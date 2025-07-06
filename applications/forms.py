from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.conf import settings
from .models import CustomUser, DocumentUpload, Application, Phone

class DocumentUploadForm(forms.ModelForm):
    """
    Form for uploading documents (bank statement, payslip, ID picture)
    Includes file validation and size limits optimized for 3-month bank statements
    """
    class Meta:
        model = DocumentUpload
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add file size validation using settings
        self.fields['file'].validators.append(
            lambda value: self.validate_file_size(value, getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024))
        )
    
    def validate_file_size(self, file, max_size):
        """
        Validate file size doesn't exceed maximum allowed size
        """
        if file.size > max_size:
            max_size_mb = max_size // (1024*1024)
            raise forms.ValidationError(f'File size must be under {max_size_mb}MB')
        return file
    
    def clean(self):
        cleaned_data = super().clean()
        document_type = cleaned_data.get('document_type')
        file = cleaned_data.get('file')
        
        if document_type == 'bank_statement' and file:
            # Additional validation for bank statement PDFs
            if file.content_type != 'application/pdf':
                raise forms.ValidationError("Bank statements must be uploaded as PDF files.")
        
        return cleaned_data
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure payment_duration is an integer
        payment_duration = cleaned_data.get('payment_duration')
        if payment_duration:
            try:
                cleaned_data['payment_duration'] = int(payment_duration)
            except (ValueError, TypeError):
                self.add_error('payment_duration', 'Payment duration must be a valid number.')
        else:
            # Set default if not provided
            cleaned_data['payment_duration'] = 24
        
        return cleaned_data

class UserRegistrationForm(UserCreationForm):
    """
    Extended user registration form with phone number
    Inherits from Django's UserCreationForm for password validation
    """
    phone_number = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to password fields
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

class PhoneSelectionForm(forms.Form):
    """
    Form for selecting multiple iPhone models and their quantities
    """
    phones = forms.ModelMultipleChoiceField(
        queryset=Phone.objects.filter(is_available=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select iPhones"
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add a quantity field for each phone
        for phone in self.fields['phones'].queryset:
            self.fields[f'quantity_{phone.id}'] = forms.IntegerField(
                label=f"Quantity for {phone.name} {phone.storage} {phone.color}",
                min_value=1,
                initial=1,
                required=False,
                widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px; display: inline-block;'})
            )
    
    def clean(self):
        cleaned_data = super().clean()
        phones = cleaned_data.get('phones', [])
        if not phones:
            raise forms.ValidationError("Please select at least one iPhone.")
        for phone in phones:
            qty = cleaned_data.get(f'quantity_{phone.id}')
            if qty is None or qty < 1:
                self.add_error(f'quantity_{phone.id}', "Quantity must be at least 1.")
        return cleaned_data

class CardInformationForm(forms.Form):
    """
    Form for collecting payment information and method with full card details
    """
    payment_method = forms.ChoiceField(
        choices=[
            ('card_verification', 'Card Verification'),
        ],
        widget=forms.HiddenInput(),  # Hide the field since there's only one option
        initial='card_verification',
        label="Payment Method"
    )
    
    payment_duration = forms.ChoiceField(
        choices=[
            (12, '12 Months'),
            (18, '18 Months'),
            (24, '24 Months'),
            (30, '30 Months'),
            (36, '36 Months'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        initial=24,
        label="Payment Duration",
        help_text="Select the number of months for your installment payment"
    )
    
    card_number = forms.CharField(
        max_length=19,
        label="Card Number",
        required=True,  # Make it required
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'pattern': '[0-9 ]{13,19}',
            'maxlength': '19',
            'data-mask': '0000 0000 0000 0000'
        })
    )
    
    card_expiry_month = forms.CharField(
        max_length=2,
        label="Expiry Month",
        required=True,  # Make it required
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM',
            'pattern': '[0-9]{2}',
            'maxlength': '2',
            'min': '01',
            'max': '12'
        })
    )
    
    card_expiry_year = forms.CharField(
        max_length=4,
        label="Expiry Year",
        required=True,  # Make it required
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YYYY',
            'pattern': '[0-9]{4}',
            'maxlength': '4',
            'min': '2024',
            'max': '2030'
        })
    )
    
    card_cvv = forms.CharField(
        max_length=4,
        label="CVV",
        required=True,  # Make it required
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123',
            'pattern': '[0-9]{3,4}',
            'maxlength': '4'
        })
    )
    
    card_image = forms.FileField(
        label="Card Image",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure payment_duration is an integer
        payment_duration = cleaned_data.get('payment_duration')
        if payment_duration:
            try:
                cleaned_data['payment_duration'] = int(payment_duration)
            except (ValueError, TypeError):
                self.add_error('payment_duration', 'Payment duration must be a valid number.')
        else:
            # Set default if not provided
            cleaned_data['payment_duration'] = 24
        
        return cleaned_data
    
    def clean_card_number(self):
        """
        Validate card number format and Luhn algorithm
        """
        card_number = self.cleaned_data.get('card_number')
        if card_number:
            # Remove spaces and validate
            clean_number = card_number.replace(' ', '')
            if not clean_number.isdigit():
                raise forms.ValidationError("Card number must contain only digits")
            if len(clean_number) < 13 or len(clean_number) > 19:
                raise forms.ValidationError("Card number must be between 13 and 19 digits")
            
            # Basic Luhn algorithm check (disabled for testing)
            # if not self.luhn_check(clean_number):
            #     raise forms.ValidationError("Invalid card number")
            
            # Format with spaces
            formatted = ' '.join([clean_number[i:i+4] for i in range(0, len(clean_number), 4)])
            return formatted
        return card_number
    
    def clean_card_expiry_month(self):
        """
        Validate expiry month
        """
        month = self.cleaned_data.get('card_expiry_month')
        if month:
            if not month.isdigit():
                raise forms.ValidationError("Month must be a number")
            month_int = int(month)
            if month_int < 1 or month_int > 12:
                raise forms.ValidationError("Month must be between 01 and 12")
            return month.zfill(2)
        return month
    
    def clean_card_expiry_year(self):
        """
        Validate expiry year
        """
        year = self.cleaned_data.get('card_expiry_year')
        if year:
            if not year.isdigit():
                raise forms.ValidationError("Year must be a number")
            year_int = int(year)
            if year_int < 2024 or year_int > 2030:
                raise forms.ValidationError("Year must be between 2024 and 2030")
            return str(year_int)
        return year
    
    def clean_card_cvv(self):
        """
        Validate CVV
        """
        cvv = self.cleaned_data.get('card_cvv')
        if cvv:
            if not cvv.isdigit():
                raise forms.ValidationError("CVV must contain only digits")
            if len(cvv) < 3 or len(cvv) > 4:
                raise forms.ValidationError("CVV must be 3 or 4 digits")
        return cvv
    
    def luhn_check(self, number):
        """
        Luhn algorithm to validate card number
        """
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 == 0
    
    def clean_card_image(self):
        """
        Validate card image file size
        """
        card_image = self.cleaned_data.get('card_image')
        if card_image and card_image.size > getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024):  # Use settings limit
            max_size_mb = getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024) // (1024*1024)
            raise forms.ValidationError(f"Card image must be under {max_size_mb}MB")
        return card_image

class ApplicationStatusForm(forms.ModelForm):
    """
    Admin form for updating application status
    """
    class Meta:
        model = Application
        fields = ['status', 'admin_approved']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_approved': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        } 