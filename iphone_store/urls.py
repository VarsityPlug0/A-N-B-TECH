"""
URL configuration for iphone_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

# Configure admin site
admin.site.site_header = "A N B TECH SUPPLIES - Admin"
admin.site.site_title = "A N B TECH SUPPLIES"
admin.site.index_title = "Welcome to A N B TECH SUPPLIES Administration"

urlpatterns = [
    path('', RedirectView.as_view(url='/applications/', permanent=False)),
    path('admin/', admin.site.urls),
    path('applications/', include('applications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
