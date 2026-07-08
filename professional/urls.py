from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path('dashboard/', views.dashboard, name='professional_dashboard'),

    # Tickets
    path('tickets/', views.tickets, name='professional_tickets'),
    path('tickets/<int:id>/', views.ticket_details, name='ticket_details'),

    # Incidents
    path('incidents/', views.incidents, name='professional_incidents'),
    path('incidents/<int:id>/', views.incident_detail, name='incident_detail'),

    # Reports
    path('reports/', views.report, name='report'),
    path("incidents/<int:pk>/upload-report/", views.upload_investigation_report, name="upload_report"),
    path('reports/<int:id>/', views.report_details, name='report_details'),
    path("reports/view/<int:pk>/", views.view_report, name="view_report"),

    # Requests
    path('request/', views.my_request, name='professional_request'),

    # Profile
    path('profile/', views.profile, name='professional_profile'),

    # Settings
    path('settings/', views.settings, name='professional_settings'),

    # Notifications
    path('notifications/', views.notifications, name='professional_notifications'),

    path(
    "services/",
    views.professional_services,
    name="professional_services"),

    
]
