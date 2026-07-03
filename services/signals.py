import uuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Ticket
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserSettings



@receiver(pre_save, sender=Ticket)
def generate_ticket_number(sender, instance, **kwargs):
    if not instance.ticket_number:
        instance.ticket_number = f"TKT-{uuid.uuid4().hex[:8].upper()}"


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)