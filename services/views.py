from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .ai import analyze_ticket
from .models import (
   Services,
    Incident,
    Ticket,
    TicketMessage,
    SecurityReport,
)
@login_required
def services(request):

    return render(
        request,
        "services/services.html"
    )


@login_required
def request_service(request):

    service = request.GET.get("service")

    if request.method == "POST":

        Services.objects.create(
            user=request.user,
            service_name=request.POST.get("service_name"),
            description=request.POST.get("description"),
        )

        messages.success(
            request,
            "Service request submitted successfully."
        )

        return redirect("services")

    return render(
        request,
        "services/request_service.html",
        {
            "service": service,
        }
    )

from django.http import HttpResponse

@login_required
def professional_services(request):
    return HttpResponse("THIS IS THE PROFESSIONAL SERVICES PAGE")





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
            description=request.POST.get("description"),
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

def create_ticket(request):
    ticket = Ticket.objects.create(
        user=request.user,
        subject=request.POST['subject'],
        message=request.POST['message']
    )

    analysis = analyze_ticket(ticket.message)

    ticket.priority = analysis["priority"]
    ticket.category = analysis["category"]
    ticket.ai_summary = analysis["reply"]
    ticket.save()

    return redirect("dashboard")


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
def ticket_detail(request, pk):

    ticket = Ticket.objects.get(
        id=pk,
        user=request.user
    )

    conversation = ticket.messages.all().order_by(
        "created_at"
    )

    return render(
        request,
        "services/ticket_detail.html",
        {
            "ticket": ticket,
            "conversation": conversation,
        }
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