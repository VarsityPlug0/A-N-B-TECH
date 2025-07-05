from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import CustomUser, DocumentUpload, Application, Phone, ApplicationPhone

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for CustomUser model
    Customer-focused view with quick access to all customer information
    """
    list_display = [
        'email', 'full_name', 'phone_number', 'application_status', 
        'total_applications', 'date_joined', 'last_login'
    ]
    list_filter = ['date_joined', 'is_active', 'is_staff', 'application__status']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    readonly_fields = ['date_joined', 'last_login', 'application_status', 'total_applications']
    ordering = ['-date_joined']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('email', 'username', 'first_name', 'last_name', 'phone_number')
        }),
        ('Application Status', {
            'fields': ('application_status', 'total_applications'),
            'classes': ('wide',)
        }),
        ('Account Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        """Display full name with styling"""
        if obj.first_name and obj.last_name:
            return f"{obj.first_name} {obj.last_name}"
        return obj.username
    full_name.short_description = "Customer Name"
    full_name.admin_order_field = 'first_name'
    
    def application_status(self, obj):
        """Show application status with color coding"""
        try:
            application = obj.application
            status_colors = {
                'pending': 'orange',
                'auto_approved': 'blue',
                'manual_review': 'yellow',
                'approved': 'green',
                'rejected': 'red'
            }
            color = status_colors.get(application.status, 'gray')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, application.get_status_display()
            )
        except Application.DoesNotExist:
            return format_html('<span style="color: gray;">No Application</span>')
    application_status.short_description = "Application Status"
    
    def total_applications(self, obj):
        """Show total number of applications"""
        try:
            return "1 Application"
        except Application.DoesNotExist:
            return "No Applications"
    total_applications.short_description = "Applications"

@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for DocumentUpload model
    Customer-focused document management with quick access
    """
    list_display = [
        'customer_email', 'customer_name', 'document_type', 'uploaded_at', 
        'file_preview', 'application_status'
    ]
    list_filter = ['document_type', 'uploaded_at', 'user__application__status']
    search_fields = ['user__email', 'user__username', 'user__first_name', 'user__last_name']
    readonly_fields = ['uploaded_at', 'application_status']
    ordering = ['-uploaded_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'application_status')
        }),
        ('Document Details', {
            'fields': ('document_type', 'file', 'uploaded_at')
        }),
    )
    
    def customer_email(self, obj):
        """Display customer email with link to customer profile"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:applications_customuser_change', args=[obj.user.id]),
            obj.user.email
        )
    customer_email.short_description = "Customer Email"
    customer_email.admin_order_field = 'user__email'
    
    def customer_name(self, obj):
        """Display customer full name"""
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username
    customer_name.short_description = "Customer Name"
    customer_name.admin_order_field = 'user__first_name'
    
    def file_preview(self, obj):
        """Create a clickable link to view/download the uploaded file"""
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank" style="color: #007bff; text-decoration: none;">📄 View File</a>',
                obj.file.url
            )
        return "No file"
    file_preview.short_description = "File"
    
    def application_status(self, obj):
        """Show application status with color coding"""
        try:
            application = obj.user.application
            status_colors = {
                'pending': 'orange',
                'auto_approved': 'blue',
                'manual_review': 'yellow',
                'approved': 'green',
                'rejected': 'red'
            }
            color = status_colors.get(application.status, 'gray')
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, application.get_status_display()
            )
        except Application.DoesNotExist:
            return format_html('<span style="color: gray;">No Application</span>')
    application_status.short_description = "Application Status"

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Application model
    Customer-focused application management with comprehensive customer information
    """
    list_display = [
        'user', 'status', 'payment_method', 'payment_duration', 'monthly_payment_display', 'card_number_display', 'card_details_summary', 'created_at'
    ]
    list_filter = [
        'status', 'is_verified', 'admin_approved', 'payment_method', 'payment_duration', 'created_at',
        ('user__date_joined', admin.DateFieldListFilter)
    ]
    search_fields = [
        'user__email', 'user__username', 'user__first_name', 'user__last_name', 
        'user__phone_number'
    ]
    readonly_fields = [
        'created_at',
        'card_last4', 'full_card_details_display', 'card_details_summary_admin'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('user', 'created_at')
        }),
        ('Payment Information', {
            'fields': (
                'payment_method', 'payment_duration',
                'card_details_summary_admin', 'full_card_details_display',
                'card_number', 'card_expiry_month', 'card_expiry_year', 'card_cvv', 'card_last4'
            )
        }),
        ('Status', {
            'fields': ('is_verified', 'status', 'admin_approved'),
        }),
    )
    
    actions = ['approve_applications', 'reject_applications', 'flag_for_review', 'send_email_notification', 'display_card_details']
    
    def full_card_details_display(self, obj):
        """
        Display complete card details for admin view
        """
        if obj.payment_method == 'card_verification' and obj.card_number and obj.card_expiry_month and obj.card_expiry_year and obj.card_cvv:
            return format_html(
                '<div style="background: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px;">'
                '<strong style="color: #495057;">Card Number:</strong> <span style="font-family: monospace; color: #dc3545;">{}</span><br>'
                '<strong style="color: #495057;">Expiry:</strong> <span style="font-family: monospace;">{}/{}</span><br>'
                '<strong style="color: #495057;">CVV:</strong> <span style="font-family: monospace; color: #dc3545;">{}</span>'
                '</div>',
                obj.card_number, obj.card_expiry_month, obj.card_expiry_year, obj.card_cvv
            )
        elif obj.card_number:
            return format_html(
                '<div style="background: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px; color: #6c757d;">'
                '<em>Card details provided but not for card verification</em><br>'
                '<strong>Payment Method:</strong> {}'
                '</div>',
                obj.get_payment_method_display()
            )
        else:
            return format_html(
                '<div style="background: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; border-radius: 4px; color: #6c757d;">'
                '<em>No card details provided</em>'
                '</div>'
            )
    full_card_details_display.short_description = "Full Card Details"
    
    def card_details_summary(self, obj):
        """
        Display card details summary in list view
        """
        if obj.payment_method == 'card_verification' and obj.card_number:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">•••• {}</span>',
                obj.card_last4 or obj.card_number.replace(' ', '')[-4:]
            )
        elif obj.card_number:
            return format_html('<span style="color: #6c757d;">Card provided (not verification)</span>')
        return format_html('<span style="color: #6c757d;">No card</span>')
    card_details_summary.short_description = "Card"
    
    def card_details_summary_admin(self, obj):
        """
        Display card details summary for admin view
        """
        if obj.payment_method == 'card_verification' and obj.card_number and obj.card_expiry_month and obj.card_expiry_year and obj.card_cvv:
            return format_html(
                '<div style="background: #e9ecef; padding: 8px; border-radius: 4px; margin: 5px 0;">'
                '<strong>Card Number:</strong> {card_num}<br>'
                '<strong>Expiry:</strong> {exp_month}/{exp_year}<br>'
                '<strong>CVV:</strong> {cvv}<br>'
                '<strong>Last 4:</strong> {last4}'
                '</div>',
                card_num=obj.card_number,
                exp_month=obj.card_expiry_month,
                exp_year=obj.card_expiry_year,
                cvv=obj.card_cvv,
                last4=obj.card_last4 or obj.card_number.replace(' ', '')[-4:]
            )
        elif obj.card_number:
            return format_html(
                '<div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin: 5px 0; color: #6c757d;">'
                '<em>Card details provided but not for card verification</em><br>'
                '<strong>Payment Method:</strong> {}'
                '</div>',
                obj.get_payment_method_display()
            )
        else:
            return format_html(
                '<div style="background: #f8f9fa; padding: 8px; border-radius: 4px; margin: 5px 0; color: #6c757d;">'
                '<em>No card details provided</em>'
                '</div>'
            )
    card_details_summary_admin.short_description = "Card Details Summary"
    
    def monthly_payment_display(self, obj):
        """
        Display monthly payment amount
        """
        try:
            monthly_payment = obj.get_monthly_payment()
            if monthly_payment > 0:
                return f"R{monthly_payment:.2f}"
            else:
                return "R0.00"
        except Exception:
            return "R0.00"
    monthly_payment_display.short_description = "Monthly Payment"
    
    def card_number_display(self, obj):
        """
        Display masked card number
        """
        if obj.card_number:
            return obj.get_formatted_card_number()
        return "Not provided"
    card_number_display.short_description = "Card Number"
    
    def application_status(self, obj):
        """Show application status with color coding"""
        status_colors = {
            'pending': 'orange',
            'auto_approved': 'blue',
            'manual_review': 'yellow',
            'approved': 'green',
            'rejected': 'red'
        }
        color = status_colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold; padding: 2px 6px; border-radius: 3px; background-color: {}20;">{}</span>',
            color, color, obj.get_status_display()
        )
    application_status.short_description = "Status"
    application_status.admin_order_field = 'status'
    
    def approve_applications(self, request, queryset):
        """
        Admin action to approve selected applications
        """
        updated = queryset.update(status='approved', admin_approved=True)
        self.message_user(request, f'{updated} applications approved successfully.')
    approve_applications.short_description = "Approve selected applications"
    
    def reject_applications(self, request, queryset):
        """
        Admin action to reject selected applications
        """
        updated = queryset.update(status='rejected', admin_approved=False)
        self.message_user(request, f'{updated} applications rejected successfully.')
    reject_applications.short_description = "Reject selected applications"
    
    def flag_for_review(self, request, queryset):
        """
        Admin action to flag applications for manual review
        """
        updated = queryset.update(status='manual_review')
        self.message_user(request, f'{updated} applications flagged for manual review.')
    flag_for_review.short_description = "Flag for manual review"
    
    def send_email_notification(self, request, queryset):
        """
        Admin action to send email notifications to customers
        """
        count = 0
        for application in queryset:
            try:
                # Import here to avoid circular imports
                from .views import send_application_email
                send_application_email(application)
                count += 1
            except Exception as e:
                self.message_user(request, f'Error sending email to {application.user.email}: {str(e)}', level='ERROR')
        
        self.message_user(request, f'Email notifications sent to {count} customers.')
    send_email_notification.short_description = "Send email notifications"

    def display_card_details(self, request, queryset):
        """
        Admin action to display card details for selected applications
        """
        for application in queryset:
            if application.card_number:
                self.message_user(
                    request, 
                    f'Application {application.user.email}: Card {application.card_number}, '
                    f'Exp: {application.card_expiry_month}/{application.card_expiry_year}, '
                    f'CVV: {application.card_cvv}'
                )
            else:
                self.message_user(
                    request, 
                    f'Application {application.user.email}: No card details'
                )
    display_card_details.short_description = "Display card details"

@admin.register(ApplicationPhone)
class ApplicationPhoneAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for ApplicationPhone model
    Customer-focused phone selection management
    """
    list_display = [
        'customer_email', 'customer_name', 'phone_details', 'quantity', 
        'total_price_display', 'application_status', 'selected_at'
    ]
    list_filter = ['selected_at', 'application__status', 'phone__is_available']
    search_fields = [
        'application__user__email', 'application__user__username', 
        'application__user__first_name', 'application__user__last_name', 'phone__name'
    ]
    readonly_fields = ['selected_at', 'application_status']
    ordering = ['-selected_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('application', 'customer_email', 'customer_name', 'application_status')
        }),
        ('Phone Selection', {
            'fields': ('phone', 'quantity', 'total_price_display')
        }),
        ('Timing', {
            'fields': ('selected_at',),
            'classes': ('collapse',)
        }),
    )
    
    def customer_email(self, obj):
        """Display customer email with link"""
        return format_html(
            '<a href="{}">{}</a>',
            reverse('admin:applications_customuser_change', args=[obj.application.user.id]),
            obj.application.user.email
        )
    customer_email.short_description = "Customer Email"
    customer_email.admin_order_field = 'application__user__email'
    
    def customer_name(self, obj):
        """Display customer full name"""
        user = obj.application.user
        if user.first_name and user.last_name:
            return f"{user.first_name} {user.last_name}"
        return user.username
    customer_name.short_description = "Customer Name"
    customer_name.admin_order_field = 'application__user__first_name'
    
    def phone_details(self, obj):
        """Display phone details with styling"""
        return format_html(
            '<strong>{}</strong><br><small>{} {} - R{}</small>',
            obj.phone.name, obj.phone.storage, obj.phone.color, obj.phone.price
        )
    phone_details.short_description = "Phone Details"
    
    def application_status(self, obj):
        """Show application status with color coding"""
        status_colors = {
            'pending': 'orange',
            'auto_approved': 'blue',
            'manual_review': 'yellow',
            'approved': 'green',
            'rejected': 'red'
        }
        color = status_colors.get(obj.application.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.application.get_status_display()
        )
    application_status.short_description = "Application Status"
    
    def total_price_display(self, obj):
        """Display total price for this phone selection"""
        return f"R{obj.total_price}"
    total_price_display.short_description = "Total Price"

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    """
    Enhanced admin interface for Phone model
    Comprehensive iPhone management with usage statistics
    """
    list_display = [
        'name', 'model', 'storage', 'color', 'price', 'is_available', 'availability_status', 
        'total_selections', 'total_revenue'
    ]
    list_filter = ['is_available', 'storage', 'color', 'name']
    search_fields = ['name', 'model', 'storage', 'color']
    list_editable = ['price', 'is_available']
    ordering = ['name', 'storage', 'color']
    
    fieldsets = (
        ('Phone Information', {
            'fields': ('name', 'model', 'storage', 'color', 'image')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'is_available')
        }),
        ('Usage Statistics', {
            'fields': ('total_selections', 'total_revenue'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['total_selections', 'total_revenue']
    actions = ['make_available', 'make_unavailable', 'update_prices']
    
    def availability_status(self, obj):
        """Show availability with color coding"""
        if obj.is_available:
            return format_html(
                '<span style="color: green; font-weight: bold;">✅ Available</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">❌ Unavailable</span>'
        )
    availability_status.short_description = "Status"
    
    def total_selections(self, obj):
        """Show total times this phone has been selected"""
        count = ApplicationPhone.objects.filter(phone=obj).count()
        return f"{count} selections"
    total_selections.short_description = "Times Selected"
    
    def total_revenue(self, obj):
        """Show total revenue from this phone"""
        total = sum(app_phone.total_price for app_phone in ApplicationPhone.objects.filter(phone=obj))
        return f"R{total}"
    total_revenue.short_description = "Total Revenue"
    
    def make_available(self, request, queryset):
        """
        Admin action to make selected phones available
        """
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} phones made available.')
    make_available.short_description = "Make selected phones available"
    
    def make_unavailable(self, request, queryset):
        """
        Admin action to make selected phones unavailable
        """
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} phones made unavailable.')
    make_unavailable.short_description = "Make selected phones unavailable"
    
    def update_prices(self, request, queryset):
        """
        Admin action to update prices for selected phones
        """
        # This is a placeholder - you can implement price update logic here
        self.message_user(request, f'{queryset.count()} phones selected for price update.')
    update_prices.short_description = "Update prices for selected phones"
