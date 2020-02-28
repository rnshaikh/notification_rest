# -*- coding: utf-8 -*-
from django.urls import path
from notifications import views

urlpatterns = [
    path('notification/', views.NotificationView.as_view(), name='notfication'),
   	path('notify/user/',  views.RegisterNotifyUser.as_view(), name='register-notification'),
   	path("notify/user/settings/", views.SettingsView.as_view(), name="notification-settings")
]
