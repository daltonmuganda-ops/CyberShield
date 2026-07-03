from django.contrib import admin
from .models import (
    Services,
    Incident,
    Ticket,
    TicketMessage,
    SecurityReport,
    UserSettings,
)

admin.site.register(Services)
admin.site.register(Incident)
admin.site.register(Ticket)
admin.site.register(SecurityReport)
admin.site.register(UserSettings)