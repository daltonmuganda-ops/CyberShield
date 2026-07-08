from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse
from .models import IncidentReport
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

        service_request = Services.objects.create(
             user=request.user,
             service_name=request.POST.get("service_name"),
             assistance_type=request.POST.get("assistance_type"),
             client_type=request.POST.get("client_type"),
             affected_device=request.POST.get("affected_device"),
             location=request.POST.get("location"),
             incident_days=request.POST.get("incident_days"),
             description=request.POST.get("description"),
             attachment=request.FILES.get("attachment"),
        )
        ai_result = analyze_ticket(service_request.description)

        ticket = Ticket.objects.create(
            user=request.user,
            subject=f"Service Request - {service_request.service_name}",
            message=service_request.description,
            priority=ai_result["priority"],
            category=ai_result["category"],
            ai_summary=ai_result["reply"],
        )

        messages.success(
            request,
            f"Service request submitted successfully. Your Ticket Number is {ticket.ticket_number}."
        )
        return redirect("services")

    return render(
        request,
        "services/request_service.html",
        {
            "service": service,
        }
    )


# =====================================
# INCIDENT REPORT
# =====================================

@login_required
def incident_report(request):

    if request.method == "POST":

        
        incident = Incident.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            attack_type=request.POST.get("attack_type"),
            description=request.POST.get("description"),
            evidence=request.FILES.get("evidence"),
        )

        # Automatically create a ticket
        # Analyze the incident using AI
        ai_result = analyze_ticket(incident.description)

        ticket = Ticket.objects.create(
            user=request.user,
            subject=incident.title,
            message=incident.description,
            priority=ai_result["priority"],
            category=ai_result["category"],
            ai_summary=ai_result["reply"],
        )
        messages.success(
            request,
            f"Incident reported successfully. Your Ticket Number is {ticket.ticket_number}."
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

    reports = IncidentReport.objects.filter(
        incident__user=request.user
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
            "profile": request.user.profile,
        }
    )


@login_required
def edit_profile(request):

    profile = request.user.profile

    if request.method == "POST":

        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.county = request.POST.get("county")
        request.user.email = request.POST.get("email")
        request.user.save()

        profile.bio = request.POST.get("bio")
        profile.phone = request.POST.get("phone")
        profile.gender = request.POST.get("gender")
        dob = request.POST.get("date_of_birth")

        if dob:
            profile.date_of_birth = dob
        else:
            profile.date_of_birth = None

        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        profile.save()

        messages.success(request, "Profile updated successfully.")

        return redirect("profile")

    return render(
        request,
        "services/edit_profile.html",
        {
            "profile": profile
        }
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

    settings = request.user.settings

    if request.method == "POST":

        settings.theme = request.POST.get("theme")

        settings.font_size = request.POST.get("font_size")

        settings.compact_layout = (
            "compact_layout" in request.POST
        )

        settings.save()

        messages.success(
            request,
            "Appearance updated successfully."
        )

        return redirect("appearance")

    return render(
        request,
        "services/appearance.html"
    )


@login_required
def privacy(request):

    settings = request.user.settings

    if request.method == "POST":

        settings.email_visibility = (
            "email_visibility" in request.POST
        )

        settings.activity_tracking = (
            "activity_tracking" in request.POST
        )

        settings.private_profile = (
            "private_profile" in request.POST
        )

        settings.two_factor_auth = (
            "two_factor_auth" in request.POST
        )

        settings.save()

        messages.success(
            request,
            "Privacy settings updated."
        )

        return redirect("privacy")

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
def notify(request):

    settings = request.user.settings

    if request.method == "POST":

        settings.email_notifications = (
            "email_notifications" in request.POST
        )

        settings.sms_notifications = (
            "sms_notifications" in request.POST
        )

        settings.push_notifications = (
            "push_notifications" in request.POST
        )

        settings.save()

        messages.success(
            request,
            "Notification settings updated successfully."
        )

        return redirect("notify")

    return render(
        request,
        "services/notify.html"
    )

@login_required
def download_report(request, pk):

    report = get_object_or_404(
        SecurityReport,
        pk=pk,
        analyst=request.user
    )

    response = HttpResponse(content_type="text/plain")

    response["Content-Disposition"] = (
        f'attachment; filename="{report.title}.txt"'
    )

    response.write("-------------------------------------\n")
    response.write("      CYBERSHIELD SECURITY REPORT\n")
    response.write("-------------------------------------\n\n")

    response.write(f"Title : {report.title}\n")
    response.write(f"User  : {request.user.get_full_name()}\n")
    response.write(f"Date  : {report.created_at.strftime('%d %B %Y')}\n\n")

    response.write("REPORT DETAILS\n")
    response.write("-------------------------------------\n")

    response.write(report.report)

    return response