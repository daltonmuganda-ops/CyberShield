from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import dashboard
urlpatterns = [
    path(
        "",
        views.dashboard,
        name="professional_dashboard"
    ),

    path('dashboard/', dashboard, name='dashboard'),

    path(
    "incidents/",
    views.incidents,
    name="professional_incidents"
    ),

    path(
        "incidents/<int:pk>/",
        views.incident_detail,
        name="incident_detail"
    ),

    path(
        "",
        views.dashboard,
        name="professional_dashboard"
    ),

    path(
        "incidents/",
        views.incidents,
        name="professional_incidents"
    ),

     # ==========================
    # Tickets
    # ==========================
    path(
        "tickets/",
        views.tickets,
        name="professional_tickets"
    ),

    path(
        "tickets/<int:pk>/",
        views.ticket_detail,
        name="professional_ticket_detail"
    ),

    # ==========================
    # Service Requests
    # ==========================
    path(
        "services/",
        views.service_requests,
        name="professional_services"
    ),

    path(
        "services/<int:pk>/",
        views.service_request_detail,
        name="professional_service_detail"
    ),

    # ==========================
    # Reports
    # ==========================
    path(
        "reports/",
        views.reports,
        name="professional_reports"
    ),

    path(
        "reports/<int:pk>/",
        views.report_detail,
        name="professional_report_detail"
    ),

    # ==========================
    # Notifications
    # ==========================
    path(
        "notifications/",
        views.notifications,
        name="professional_notifications"
    ),

    # ==========================
    # Profile
    # ==========================
    path(
        "profile/",
        views.profile,
        name="professional_profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="professional_edit_profile"
    ),

    path(
        "change-password/",
        views.change_password,
        name="professional_change_password"
    ),

    # ==========================
    # Settings
    # ==========================
    path(
        "settings/",
        views.settings,
        name="professional_settings"
    ),

    path(
        "settings/appearance/",
        views.appearance,
        name="professional_appearance"
    ),

    path(
        "settings/privacy/",
        views.privacy,
        name="professional_privacy"
    ),

    path(
        "settings/account/",
        views.account,
        name="professional_account"
    ),

    path(
        "delete-account/",
        views.delete_account,
        name="professional_delete_account"
    ),
    path(
        "settings/appearance/",
        views.appearance,
        name="appearance"
    ),

    path(
        "settings/privacy/",
        views.privacy,
        name="privacy"
    ),

    path(
        "settings/account/",
        views.account,
        name="account"
    ),

    path(
        "delete-account/",
        views.delete_account,
        name="delete_account"
    ),

    
    path(
        "settings/appearance/",
        views.appearance,
        name="appearance"
    ),

    path(
        "settings/privacy/",
        views.privacy,
        name="privacy"
    ),

    path(
        "settings/account/",
        views.account,
        name="account"
    ),

    path(
        "delete-account/",
        views.delete_account,
        name="delete_account"
    ),


]