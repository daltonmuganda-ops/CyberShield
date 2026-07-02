from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from services.models import SecurityReport
from .models import Notification
from django.shortcuts import render, redirect
from django.contrib.auth import login
from services.models import (
    Incident,
    ServiceRequest,
    Ticket,
    SecurityReport,
)



def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, professional)
            return redirect("professional_dashboard")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "professional/login.html")


def logout_view(request):
    logout(request)
    return redirect("home")



# =====================================
# PROFESSIONAL DASHBOARD
# =====================================

@login_required
def dashboard(request):

    context = {
        "total_incidents": Incident.objects.count(),
        "pending_incidents": Incident.objects.filter(
            status="Pending"
        ).count(),
        "investigating_incidents": Incident.objects.filter(
            status="Investigating"
        ).count(),
        "resolved_incidents": Incident.objects.filter(
            status="Resolved"
        ).count(),

        "total_services": ServiceRequest.objects.count(),
        "open_tickets": Ticket.objects.filter(
            status="Open"
        ).count(),

        "recent_incidents": Incident.objects.order_by(
            "-created_at"
        )[:5],
    }

    return render(
        request,
        "professional/dashboard.html",
        context
    )


# =====================================
# INCIDENT MANAGEMENT
# =====================================

@login_required
def incidents(request):

    context = {
        "incidents": Incident.objects.order_by("-created_at"),

        "pending": Incident.objects.filter(
            status="Pending"
        ).count(),

        "investigating": Incident.objects.filter(
            status="Investigating"
        ).count(),

        "resolved": Incident.objects.filter(
            status="Resolved"
        ).count(),
    }

    return render(
        request,
        "professional/incident.html",
        context
    )


# =====================================
# INCIDENT DETAILS
# =====================================

@login_required
def incident_detail(request, pk):

    incident = get_object_or_404(
        Incident,
        pk=pk
    )

    analysts = User.objects.filter(
        is_staff=True
    )

    if request.method == "POST":

        incident.status = request.POST.get("status")

        incident.priority = request.POST.get("priority")

        incident.investigation_notes = request.POST.get(
            "investigation_notes"
        )

        analyst = request.POST.get("assigned_to")

        if analyst:
            incident.assigned_to = User.objects.get(
                id=analyst
            )

        if request.FILES.get("investigation_report"):
            incident.investigation_report = request.FILES.get(
                "investigation_report"
            )

        if incident.status == "Resolved":
            incident.resolved_at = timezone.now()

        incident.save()

        messages.success(
            request,
            "Incident updated successfully."
        )

        return redirect(
            "professional_incidents"
        )

    return render(
        request,
        "professional/incident_details.html",
        {
            "incident": incident,
            "analysts": analysts,
        }
    )


# =====================================
# SERVICE REQUESTS
# =====================================

@login_required
def service_requests(request):

    requests = ServiceRequest.objects.order_by(
        "-created_at"
    )

    return render(
        request,
        "professional/services.html",
        {
            "requests": requests
        }
    )


@login_required
def service_request_detail(request, pk):

    service = get_object_or_404(
        ServiceRequest,
        pk=pk
    )

    if request.method == "POST":

        service.status = request.POST.get("status")

        service.analyst_comment = request.POST.get(
            "analyst_comment"
        )

        service.save()

        messages.success(
            request,
            "Service request updated."
        )

        return redirect(
            "professional_services"
        )

    return render(
        request,
        "professional/service_detail.html",
        {
            "service": service
        }
    )


# =====================================
# SUPPORT TICKETS
# =====================================

@login_required
def tickets(request):

    tickets = Ticket.objects.order_by(
        "-created_at"
    )

    return render(
        request,
        "professional/tickets.html",
        {
            "tickets": tickets
        }
    )


@login_required
def ticket_detail(request, pk):

    ticket = get_object_or_404(
        Ticket,
        pk=pk
    )

    if request.method == "POST":

        ticket.status = request.POST.get("status")

        ticket.save()

        messages.success(
            request,
            "Ticket updated."
        )

        return redirect(
            "professional_tickets"
        )

    return render(
        request,
        "professional/ticket_detail.html",
        {
            "ticket": ticket
        }
    )


# =====================================
# REPORTS
# =====================================

@login_required
def reports(request):

    reports = SecurityReport.objects.order_by(
        "-created_at"
    )

    return render(
        request,
        "professional/report.html",
        {
            "report": reports
        }
    )


# =====================================
# NOTIFICATIONS
# =====================================

@login_required
def notifications(request):

    return render(
        request,
        "professional/notifications.html"
    )


# =====================================
# PROFILE
# =====================================

@login_required
def profile(request):

    return render(
        request,
        "professional/profile.html"
    )

@login_required
def notifications(request):
    notifications = Notification.objects.order_by("-created_at")

    return render(
        request,
        "professional/notifications.html",
        {
            "notifications": notifications
        }
    )
@login_required
def settings(request):
    return render(
        request,
        "professional/settings.html"
    )
@login_required
def report_detail(request, pk):

    report = get_object_or_404(
        SecurityReport,
        pk=pk
    )

    return render(
        request,
        "professional/report_detail.html",
        {
            "report": report
        }
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

