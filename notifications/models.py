from django.db import models
# Create your models here.
from enum import Enum

class NotificationType(Enum):

    NOTIFICATION1 = "notification1"
    NOTIFICATION2 = "notification2"
    NOTIFICATION3 = "notification3"

    @classmethod
    def as_tuple(cls):
        return ((item.value, item.name.replace('_', ' ')) for item in cls)

class UserChannel(models.Model):

    user =  models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    notification_type = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)


class Notification(models.Model):

    receiver = models.CharField(max_length=500)
    message = models.TextField(blank=True, null=True)
    notfication_type = models.CharField(max_length=500, choices=NotificationType.as_tuple())


class UserBindings(models.Model):

    user = models.CharField(max_length=500)
    sid = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    binding_type =models.CharField(max_length=500)