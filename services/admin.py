from django.contrib import admin
from .models import (
    ServiceRequest,
    Incident,
    Ticket,
    SecurityReport,
    UserSettings
)

admin.site.register(ServiceRequest)
admin.site.register(Incident)
admin.site.register(Ticket)
admin.site.register(SecurityReport)
admin.site.register(UserSettings)