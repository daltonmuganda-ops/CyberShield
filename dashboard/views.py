from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from services.models import (
    Services,
    Incident,
    Ticket,
    SecurityReport,
)


# Home page
def home(request):
    return render(request, "dashboard/home.html")


# Dashboard page
@login_required(login_url="login")
def dashboard(request):

    requests = Services.objects.filter(user=request.user).count()

    incidents = Incident.objects.filter(user=request.user).count()

    tickets = Ticket.objects.filter(user=request.user).count()

    # ✅ FIXED LINE
    reports = SecurityReport.objects.filter(
        service__user=request.user
    ).count()

    context = {
        "requests": requests,
        "incidents": incidents,
        "tickets": tickets,
        "reports": reports,
    }

    return render(request, "dashboard/dashboard.html", context)