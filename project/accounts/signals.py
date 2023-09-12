from django.contrib.auth.models import AbstractUser
from . import models
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=AbstractUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        models.User.objects.create(user=instance)

@receiver(post_save, sender=AbstractUser)
def save_profile(sender, instance, **kwargs):
        instance.User.save()
        