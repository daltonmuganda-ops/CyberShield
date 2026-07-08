from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from services.models import UserSettings
from django.contrib.auth.models import User
from services.models import (
    Services,
    Ticket,
    Incident,
    SecurityReport,
    IncidentReport,
)


def is_analyst(user):
    return user.is_authenticated and hasattr(user, "settings") and user.settings.role == "analyst"



# DASHBOARD
@login_required
def dashboard(request):
    if not is_analyst(request.user):
        return redirect("user_dashboard")

    total_incidents = Incident.objects.count()

    open_tickets = Ticket.objects.filter(status="Open").count()
    in_progress_tickets = Ticket.objects.filter(status="In Progress").count()
    closed_tickets = Ticket.objects.filter(status="Closed").count()

    investigating_incidents = Incident.objects.filter(
        status="Investigating"
    ).count()

    resolved_incidents = Incident.objects.filter(
        status="Resolved"
    ).count()

    service_requests = Services.objects.filter(
        status="Pending"
    ).count()

    latest_incidents = Incident.objects.order_by("-created_at")[:5]
    latest_tickets = Ticket.objects.order_by("-created_at")[:5]
    latest_requests = Services.objects.filter(
        status="Pending"
    ).order_by("-created_at")[:5]

    
    return render(request, "professional/dashboard.html", {
        "total_incidents": total_incidents,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "closed_tickets": closed_tickets,
        "investigating_incidents": investigating_incidents,
        "resolved_incidents": resolved_incidents,
        "service_requests": service_requests,
        "latest_incidents": latest_incidents,
        "latest_tickets": latest_tickets,
        "latest_requests": latest_requests,
    })

# SERVICE REQUESTS

@login_required
def my_request(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    request = Services.objects.all().order_by("-created_at")

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


# TICKETS

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


# INCIDENTS
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

    incident = get_object_or_404(Incident, id=id)

    analysts = User.objects.filter(is_staff=True)  # or your analyst group

    if request.method == "POST":

        incident.status = request.POST.get("status")
        incident.priority = request.POST.get("priority")
        incident.investigation_notes = request.POST.get("investigation_notes")

        assigned_id = request.POST.get("assigned_to")

        if assigned_id:
            incident.assigned_to = User.objects.get(id=assigned_id)
        else:
            incident.assigned_to = None

        if request.FILES.get("investigation_report"):
            incident.investigation_report = request.FILES["investigation_report"]

        incident.save()
        # CREATE INVESTIGATION REPORT
        IncidentReport.objects.create(

            incident=incident,

            analyst=request.user,

            title=f"Investigation Report - {incident.title}",

            report=incident.investigation_report,

            recommendations=incident.investigation_notes,

            status="Completed"

        )

        return redirect("incident_detail", id=incident.id)

    return render(request, "professional/incident_details.html", {
        "incident": incident,
        "analysts": analysts
    })


# REPORTS
@login_required
def report(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    reports = IncidentReport.objects.all().order_by("-created_at")

    return render(request, "professional/report.html", {
        "reports": reports
    })


@login_required
def report_details(request, id):
    if not is_analyst(request.user):
        return redirect("dashboard")

    report = SecurityReport.objects.get(id=id)

    return render(request, "professional/report_detail.html", {
        "report": report
    })

@login_required
def reports_list(request):
    reports = SecurityReport.objects.select_related("service", "analyst")
    return render(request, "professional/reports.html", {"reports": reports})


def upload_investigation_report(request, pk):
    incident = get_object_or_404(Incident, pk=pk)

    if request.method == "POST":
        incident.investigation_report = request.FILES.get("investigation_report")
        incident.save()

        return redirect("incident_detail", pk=incident.id)

    return render(request, "professional/upload_report.html", {"incident": incident}
    )
@login_required
def view_report(request, pk):
    report = get_object_or_404(IncidentReport, id=pk)
    return render(request, "professional/view_report.html", {"report": report})



# PROFILE
@login_required
def profile(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    return render(request, "professional/profile.html")



# SETTINGS


@login_required
def settings(request):
    if not is_analyst(request.user):
        return redirect("dashboard")

    settings, created = UserSettings.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        settings.theme = request.POST.get("theme")
        settings.font_size = request.POST.get("font_size")

        settings.private_profile = (
            request.POST.get("private_profile") == "on"
        )

        settings.email_notifications = (
            request.POST.get("email_notifications") == "on"
        )

        settings.push_notifications = (
            request.POST.get("push_notifications") == "on"
        )

        settings.save()

        messages.success(
            request,
            "Settings updated successfully."
        )

        return redirect("professional_settings")

    return render(
        request,
        "professional/settings.html",
        {
            "settings": settings
        }
    )
# NOTIFICATIONS
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