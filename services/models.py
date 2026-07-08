from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string
import uuid



class Services(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
    ]

    CLIENT_CHOICES = [
        ("Personal", "Personal"),
        ("Company", "Company"),
    ]

    ASSISTANCE_CHOICES = [
        ("Prevention", "Prevention"),
        ("Inspection", "Inspection"),
        ("Incident Response", "Incident Response"),
    ]

    DEVICE_CHOICES = [
        ("Desktop", "Desktop"),
        ("Laptop", "Laptop"),
        ("Mobile Phone", "Mobile Phone"),
        ("Tablet", "Tablet"),
        ("Server", "Server"),
        ("Network", "Network"),
        ("Website", "Website"),
        ("Other", "Other"),
    ]
    


    user = models.ForeignKey(User, on_delete=models.CASCADE)

    service_name = models.CharField(max_length=200)

    # NEW FIELDS
    client_type = models.CharField(
        max_length=20,
        choices=CLIENT_CHOICES,
        default="Personal"
        
    )

    assistance_type = models.CharField(
        max_length=30,
        choices=ASSISTANCE_CHOICES,
        default="Inspection"
    )

    affected_device = models.CharField(
        max_length=50,
        choices=DEVICE_CHOICES,
        default="Other"
    )

    location = models.CharField(
        max_length=200,
        default="Unknown"
    )
    incident_days = models.PositiveIntegerField(
    default=0
    )  

    incident_days = models.PositiveIntegerField()

    description = models.TextField()

    attachment = models.FileField(
        upload_to="service_requests/",
        blank=True,
        null=True
    )
    
    # Contact Information
    contact_name = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    contact_email = models.EmailField(
        blank=True,
        default=""
    )

    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )

# Contact Information
    contact_name = models.CharField(
        max_length=150,
        blank=True,
        default=""
    )

    contact_email = models.EmailField(
        blank=True,
        default=""
    )

    contact_phone = models.CharField(
        max_length=20,
        blank=True,
        default=""
    )
    

    # Service Description
    description = models.TextField()

    attachment = models.FileField(
        upload_to="service_requests/",
        blank=True,
        null=True
    )

    

    service_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    analyst = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_services"
    )

    analyst_comment = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service_name} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.service_number:
            self.service_number = f"SRV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

# INCIDENT REPORT

class Incident(models.Model):

    ATTACK_TYPES = [
        ("Malware", "Malware"),
        ("Phishing", "Phishing"),
        ("Ransomware", "Ransomware"),
        ("DDoS", "DDoS"),
        ("Unauthorized Access", "Unauthorized Access"),
        ("Data Breach", "Data Breach"),
        ("Social Engineering", "Social Engineering"),
        ("Password Attack", "Password Attack"),
        ("Website Defacement", "Website Defacement"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Investigating", "Investigating"),
        ("Resolved", "Resolved"),
    ]

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    # Student who reported the incident
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="reported_incidents")

    

    # Incident information
    title = models.CharField(max_length=200)

    attack_type = models.CharField(
        max_length=50,
        choices=ATTACK_TYPES
    )

    description = models.TextField()

    evidence = models.FileField(
        upload_to="incident_evidence/",
        blank=True,
        null=True
    )

    # Investigation information
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    # Cybersecurity analyst assigned to investigate
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="assigned_incidents"
    )

    # Analyst notes
    investigation_notes = models.TextField(
        blank=True,
        null=True
    )

    # Final investigation report
    investigation_report = models.FileField(
        upload_to="investigation_reports/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    resolved_at = models.DateTimeField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} ({self.status})"


# SUPPORT TICKET
class Ticket(models.Model):

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
    ]

    ticket_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        blank=True
    )
    

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tickets"
    )

    service_request = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tickets"
    )

    subject = models.CharField(max_length=200)

    message = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="Medium"
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    ai_summary = models.TextField(
        blank=True,
        default=""
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            today = timezone.now().strftime("%Y%m%d")
            last_ticket = Ticket.objects.order_by("-id").first()

            if last_ticket:
                try:
                    last_number = int(last_ticket.ticket_number.split("-")[-1])
                except:
                    last_number = last_ticket.id
            else:
                last_number = 0

            self.ticket_number = f"CYB-{today}-{last_number + 1:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number} - {self.subject}"


class TicketMessage(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    is_ai = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender.username} - {self.ticket.subject}"

# SECURITY REPORT

class SecurityReport(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Completed", "Completed"),
    ]

    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        related_name="reports"
    )

    analyst = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_reports"
    )
    

    title = models.CharField(max_length=200)

    report = models.TextField()

    recommendations = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title

# USER SETTINGS


class UserSettings(models.Model):

    ROLE_CHOICES = [
        ("user", "User"),
        ("analyst", "Analyst"),
        ("admin", "Admin"),
    ]

    
    # APPEARANCE SETTINGS
    THEME_CHOICES = [
        ("light", "Light"),
        ("dark", "Dark"),
        ("system", "System"),
    ]

    FONT_CHOICES = [
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="settings"
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user"
    )


    theme = models.CharField(
        max_length=20,
        choices=THEME_CHOICES,
        default="light"
    )

    font_size = models.CharField(
        max_length=20,
        choices=FONT_CHOICES,
        default="medium"
    )

    compact_layout = models.BooleanField(default=False)

    # PRIVACY SETTINGS
    email_visibility = models.BooleanField(default=True)
    activity_tracking = models.BooleanField(default=True)
    private_profile = models.BooleanField(default=False)

    # NOTIFICATIONS
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    # SECURITY
    two_factor_auth = models.BooleanField(default=False)

    # ACCOUNT SETTINGS
    allow_data_download = models.BooleanField(default=True)
    allow_account_deletion = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Settings"

# INCIDENT INVESTIGATION REPORT

class IncidentReport(models.Model):

    STATUS_CHOICES = [
        ("Draft", "Draft"),
        ("Completed", "Completed"),
    ]

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name="incident_reports"
    )

    analyst = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="incident_reports"
    )

    title = models.CharField(
        max_length=200
    )

    report = models.FileField(
        upload_to="investigation_reports/",
        blank=True,
        null=True
    )

    recommendations = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Draft"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.title


