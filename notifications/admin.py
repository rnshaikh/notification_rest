from django.contrib import admin

from notifications.models import UserChannel, Notification, UserBindings

# Register your models here.

admin.site.register(Notification)
admin.site.register(UserChannel)
admin.site.register(UserBindings)
