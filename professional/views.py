from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from services.models import (
    Services,
    Ticket,
    Incident,
    SecurityReport,
)


def is_analyst(user):
    return user.is_authenticated and hasattr(user, "settings") and user.settings.role == "analyst"


# ==========================
# DASHBOARD
# ==========================
@login_required
def dashboard(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    open_tickets = Ticket.objects.filter(status="Open").order_by("-created_at")
    in_progress_tickets = Ticket.objects.filter(status="In Progress").order_by("-created_at")
    closed_tickets = Ticket.objects.filter(status="Closed").order_by("-created_at")

    open_incidents = Incident.objects.filter(status="Pending").order_by("-created_at")
    investigating_incidents = Incident.objects.filter(status="Investigating").order_by("-created_at")
    resolved_incidents = Incident.objects.filter(status="Resolved").order_by("-created_at")

    service_requests = Services.objects.filter(status="Pending").order_by("-created_at")


    return render(request, "professional/dashboard.html", {
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "closed_tickets": closed_tickets,
        "open_incidents": open_incidents,
        "investigating_incidents": investigating_incidents,
        "resolved_incidents": resolved_incidents,
        "service_requests": service_requests,
    })


# ==========================
# SERVICE REQUESTS
# ==========================
@login_required
def my_request(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    request = MyRequest.objects.all().order_by("-created_at")

    return render(request, "professional/request.html", {
        "requests": requests
    })


@login_required
def request_detail(request, id):
    if not is_analyst(request.user):
        return redirect("dashboard")

    request_obj = MyRequest.objects.get(id=id)

    return render(request, "professional/request_detail.html", {
        "request": request_obj
    })


# ==========================
# TICKETS
# ==========================
@login_required
def tickets(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    tickets = Ticket.objects.all().order_by("-created_at")

    return render(request, "professional/tickets.html", {
        "tickets": tickets
    })


@login_required
def ticket_details(request, id):
    if not is_analyst(request.user):
        return redirect("dashboard")

    ticket = Ticket.objects.get(id=id)

    return render(request, "professional/ticket_detail.html", {
        "ticket": ticket
    })


# ==========================
# INCIDENTS
# ==========================
@login_required
def incidents(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    incidents = Incident.objects.all().order_by("-created_at")

    return render(request, "professional/incidents.html", {
        "incidents": incidents
    })


@login_required
def incident_detail(request, id):
    if not is_analyst(request.user):
        return redirect("dashboard")

    incident = Incident.objects.get(id=id)

    return render(request, "professional/incident_detail.html", {
        "incident": incident
    })


# ==========================
# REPORTS
# ==========================
@login_required
def report(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    reports = SecurityReport.objects.all().order_by("-created_at")

    return render(request, "professional/report.html", {
        "report": report
    })


@login_required
def report_details(request, id):
    if not is_analyst(request.user):
        return redirect("dashboard")

    report = SecurityReport.objects.get(id=id)

    return render(request, "professional/report_detail.html", {
        "report": report
    })


# ==========================
# PROFILE
# ==========================
@login_required
def profile(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    return render(request, "professional/profile.html")


# ==========================
# SETTINGS
# ==========================
@login_required
def settings(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    return render(request, "professional/settings.html")


# ==========================
# NOTIFICATIONS
# ==========================
@login_required
def notifications(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    return render(request, "professional/notifications.html")

@login_required
def professional_services(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    services = Services.objects.all().order_by("-created_at")

    return render(
        request,
        "professional/services.html",
        {
            "services": services,
        },
    )