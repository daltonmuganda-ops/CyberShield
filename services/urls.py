from django.urls import path
from . import views

urlpatterns = [

    path("", views.services, name="services"),

    path(
        "request_service/",
        views.request_service,
        name="request_service"
    ),

    path(
        "incident/",
        views.incident_report,
        name="incident"
    ),

    path(
        "tickets/",
        views.tickets,
        name="tickets"
    ),

    path(
        "create-ticket/",
        views.create_ticket,
        name="create_ticket"
    ),

    path(
        "reports/",
        views.reports,
        name="reports"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "edit_profile/",
        views.edit_profile,
        name="edit_profile"
    ),

    path(
        "change_password/",
        views.change_password,
        name="change_password"
    ),

    path(
        "notifications/",
        views.notifications,
        name="notifications"
    ),

    path(
        "settings/",
        views.settings,
        name="settings"
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