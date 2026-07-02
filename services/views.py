from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .models import (
    ServiceRequest,
    Incident,
    Ticket,
    SecurityReport,
)


# =====================================
# SERVICES HOME
# =====================================

@login_required
def services(request):

    return render(
        request,
        "services/services.html"
    )


# =====================================
# SERVICE REQUESTS
# =====================================

@login_required
def request_service(request):

    if request.method == "POST":

        ServiceRequest.objects.create(
            user=request.user,
            service_name=request.POST.get("service_name"),
            description=request.POST.get("description"),
        )

        messages.success(
            request,
            "Service request submitted successfully."
        )

        return redirect("request_service")

    requests = ServiceRequest.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "services/request_service.html",
        {
            "requests": requests
        }
    )


# =====================================
# INCIDENT REPORT
# =====================================

@login_required
def incident_report(request):

    if request.method == "POST":

        Incident.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            attack_type=request.POST.get("attack_type"),
            statement=request.POST.get("statement"),
            evidence=request.FILES.get("evidence"),
        )

        messages.success(
            request,
            "Incident reported successfully."
        )

        return redirect("incident")

    incidents = Incident.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "services/incident.html",
        {
            "incidents": incidents
        }
    )


# =====================================
# TICKETS
# =====================================

@login_required
def tickets(request):

    tickets = Ticket.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "services/tickets.html",
        {
            "tickets": tickets
        }
    )


@login_required
def create_ticket(request):

    if request.method == "POST":

        Ticket.objects.create(
            user=request.user,
            subject=request.POST.get("subject"),
            message=request.POST.get("message"),
        )

        messages.success(
            request,
            "Ticket created successfully."
        )

        return redirect("tickets")

    return render(
        request,
        "services/create_ticket.html"
    )


# =====================================
# REPORTS
# =====================================

@login_required
def reports(request):

    reports = SecurityReport.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "services/reports.html",
        {
            "reports": reports
        }
    )


# =====================================
# PROFILE
# =====================================

@login_required
def profile(request):

    return render(
        request,
        "services/profile.html",
        {
            "user": request.user
        }
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        user = request.user

        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "services/edit_profile.html"
    )


# =====================================
# CHANGE PASSWORD
# =====================================

@login_required
def change_password(request):

    if request.method == "POST":

        user = request.user

        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")

        if not user.check_password(old_password):

            messages.error(
                request,
                "Current password is incorrect."
            )

        elif new_password1 != new_password2:

            messages.error(
                request,
                "Passwords do not match."
            )

        else:

            user.set_password(new_password1)
            user.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

    return render(
        request,
        "services/change_password.html"
    )


# =====================================
# NOTIFICATIONS
# =====================================

@login_required
def notifications(request):

    return render(
        request,
        "services/notifications.html"
    )


# =====================================
# SETTINGS
# =====================================

@login_required
def settings(request):

    return render(
        request,
        "services/settings.html"
    )


@login_required
def appearance(request):

    return render(
        request,
        "services/appearance.html"
    )


@login_required
def privacy(request):

    return render(
        request,
        "services/privacy.html"
    )


@login_required
def account(request):

    return render(
        request,
        "services/account.html"
    )


@login_required
def delete_account(request):

    messages.info(
        request,
        "Delete account feature coming soon."
    )

    return redirect("account")