from django.db import models
from django.contrib.auth.models import User


# ==========================
# SERVICE REQUEST
# ==========================

class ServiceRequest(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    service_name = models.CharField(max_length=200)

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.service_name} - {self.user.username}"
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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.subject


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

    # Appearance
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

    compact_layout = models.BooleanField(
        default=False
    )

    # Privacy
    email_visibility = models.BooleanField(
        default=True
    )

    activity_tracking = models.BooleanField(
        default=True
    )

    private_incidents = models.BooleanField(
        default=True
    )

    two_factor_auth = models.BooleanField(
        default=False
    )

    # Notifications
    email_notifications = models.BooleanField(
        default=True
    )

    sms_notifications = models.BooleanField(
        default=False
    )

    push_notifications = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} Settings"

analyst_comment = models.TextField(
    blank=True,
    null=True
)