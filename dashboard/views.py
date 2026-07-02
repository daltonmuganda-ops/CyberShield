from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from services.models import (ServiceRequest,Incident,Ticket,SecurityReport,)


# Home page
def home(request):
    return render(request, "dashboard/home.html")


# Dashboard page
@login_required(login_url="login")
def dashboard(request):

    requests = ServiceRequest.objects.filter(
        user=request.user
    ).count()

    incidents = Incident.objects.filter(
        user=request.user
    ).count()
    
    tickets = Ticket.objects.filter(
        user=request.user
    ).count()

    reports = SecurityReport.objects.filter(
        user=request.user
    ).count()

    context = {
        "requests": requests,
        "incidents": incidents,
        "tickets": tickets,
        "reports": reports,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )