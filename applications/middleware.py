import logging
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

logger = logging.getLogger(__name__)

class AdminAccessMiddleware:
    """
    Middleware to protect admin URLs and log unauthorized access attempts
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for admin URLs
        if request.path.startswith('/applications/admin/'):
            # If user is not authenticated, redirect to login
            if not request.user.is_authenticated:
                messages.error(request, "Please log in to access this page.")
                return redirect('applications:landing_page')
            
            # If user is not staff, log the attempt and redirect
            if not request.user.is_staff:
                logger.warning(
                    f"Unauthorized admin access attempt by user {request.user.email} "
                    f"({request.user.id}) to {request.path}"
                )
                messages.error(request, "Access denied. Admin privileges required.")
                return redirect('applications:dashboard')
        
        response = self.get_response(request)
        return response 