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

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    service_name = models.CharField(max_length=200)

    description = models.TextField()

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
# ==========================
# INCIDENT REPORT
# ==========================

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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reported_incidents"
    )

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
# ==========================
# SUPPORT TICKET
# ==========================

def generate_ticket_number():
    while True:
        year = timezone.now().year

        random_code = "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6
            )
        )

        ticket_number = f"TKT-{year}-{random_code}"

        if not Ticket.objects.filter(ticket_number=ticket_number).exists():
            return ticket_number

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

    created_at = models.DateTimeField(
        auto_now_add=True
    )

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

# ==========================
# SECURITY REPORT
# ==========================

class SecurityReport(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    report = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# ==========================
# USER SETTINGS
# ==========================


class UserSettings(models.Model):

    ROLE_CHOICES = [
        ("user", "User"),
        ("analyst", "Analyst"),
        ("admin", "Admin"),
    ]

    
    # ==========================
    # APPEARANCE SETTINGS
    # ==========================
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

    # ==========================
    # PRIVACY SETTINGS
    # ==========================
    email_visibility = models.BooleanField(default=True)
    activity_tracking = models.BooleanField(default=True)
    private_profile = models.BooleanField(default=False)

    # ==========================
    # NOTIFICATIONS
    # ==========================
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    # ==========================
    # SECURITY
    # ==========================
    two_factor_auth = models.BooleanField(default=False)

    # ==========================
    # ACCOUNT SETTINGS
    # ==========================
    allow_data_download = models.BooleanField(default=True)
    allow_account_deletion = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Settings"




