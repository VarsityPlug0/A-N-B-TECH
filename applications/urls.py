from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # Main application flow
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('card-activation/', views.card_activation, name='card_activation'),
    path('select-phone/', views.select_phone, name='select_phone'),
    path('logout/', views.logout_view, name='logout'),
    path('card-information/', views.card_information, name='card_information'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin functions
    path('admin/applications/', views.admin_application_list, name='admin_application_list'),
    path('admin/applications/<int:application_id>/', views.admin_application_detail, name='admin_application_detail'),
    path('admin/test-card-details/', views.test_card_details, name='test_card_details'),
] 