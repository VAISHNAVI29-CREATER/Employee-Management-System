
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    if created:
        logger.info(
            "New user created: %s",
            instance.username
        )


@receiver(post_save, sender=Employee)
def employee_created_signal(sender, instance, created, **kwargs):
    if created:
        logger.info(
            "New employee created: %s",
            instance.name
        )
