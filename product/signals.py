from django.contrib.auth.models import User
from django.db.models.signals import pre_save


def update_user(sender, instance, **kwargs):
    if instance.email != "":
        instance.username = instance.email


pre_save.connect(sender=User, receiver=update_user)
