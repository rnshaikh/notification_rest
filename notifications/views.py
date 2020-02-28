import random
import string 

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.status import (
    HTTP_412_PRECONDITION_FAILED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.response import Response
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import (
    SyncGrant,
    VideoGrant,
    ChatGrant
)


from notifications.models import (UserChannel, Notification, UserBindings)
from notifications.serializers import NotificationSerializer
from notification_poc import constants
import time

class NotificationView(ListCreateAPIView):

    Model = Notification
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def post(self,request):

        #identity = request.data['identity']

        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY
        api_secret = settings.TWILIO_API_SECRET
        service_sid = settings.TWILIO_NOTIFICATION_SERVICE_SID

        # Initialize the Twilio client
        client = Client(api_key, api_secret, account_sid)

        service = client.notify.services(service_sid)

        # user = UserChannel.objects.filter(user='parsad1')
        # address = random.getrandbits(128)
        # msg = "This is is new message................"

        # # identity = ''.join(random.choices(string.ascii_uppercase +
        # #                      string.digits, k = 7))

        
        # content = {
        #     "identity": 'parsad1',
        #     "address": str(address),
        #     "binding_type": "fcm"
        # }


        # body = {
        #     "user": 'parsad1',
        #     "address": str(address),
        # }


        # binding = service.bindings.create(**content)
        # user = UserChannel.objects.update_or_create(**body)

        # user = user[0] if len(user) else user

        # content = {
        #     "identity": user.user,
        #     "body": msg

        # }

        notification_responses = []
        for notification_type in constants.NOTIFICATION_TYPE:
            content = {
                # "identity": identity,
                "tag": [notification_type],
                "body": "This notification type is"+notification_type
            }
            notification_response  = service.notifications.create(**content)
            notification_responses.append(notification_response._properties)
            time.sleep(3)

        # notification_response = service.notifications.create(**content)



        return Response({
            "success": True,
            "msg": "notification send successfully",
            "data": notification_responses
        })

class RegisterNotifyUser(ListCreateAPIView):

    Model = UserChannel

    def post(self,request):


        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY
        api_secret = settings.TWILIO_API_SECRET
        service_sid = settings.TWILIO_NOTIFICATION_SERVICE_SID

        # Initialize the Twilio client
        client = Client(api_key, api_secret, account_sid)

        service = client.notify.services(service_sid)

        data = request.data
        if('token' not in data):
            return Response("token is required.......",
                            status=HTTP_412_PRECONDITION_FAILED)

        # body = {
        #     "user": data['identity'],
        #     "address": data['token']
        # }

        # content = {
        #     "identity": data['identity'],
        #     "address": data['token'],
        #     "binding_type": "fcm",
        #     "tag": ["notification1"]
        # }

        #binding = service.bindings.create(**content)

        user_bindings = []
        content = {
            "identity": data['identity'],
            "address": data['token'],
            "binding_type": "fcm",
            "tag": ['notification1','notification2','notification3']
        }
        binding = service.bindings.create(**content)
        body = {
            "user": data['identity'],
            "address": data['token'],
            "binding_type":  binding._properties['binding_type'],
            "sid": binding._properties['sid']
        }
        user_binding = UserBindings.objects.update_or_create(**body, defaults={"user": data['identity']})
        print("UserBindings", user_bindings)
        #user, created  = UserChannel.objects.update_or_create(**body)

        # response = {
        #     "user": user.user,
        #     "address": user.address
        # }

        return Response({
            "success": True,
            "msg": "notification send successfully",
        })

class SettingsView(CreateAPIView):

    model = Notification

    def post(self,request):


        account_sid = settings.TWILIO_ACCOUNT_SID
        api_key = settings.TWILIO_API_KEY
        api_secret = settings.TWILIO_API_SECRET
        service_sid = settings.TWILIO_NOTIFICATION_SERVICE_SID

        # Initialize the Twilio client
        client = Client(api_key, api_secret, account_sid)

        service = client.notify.services(service_sid)

        data = request.data
        notification_type_tags = []

        if data['notification_type1']:
            notification_type_tags.append('notification1')

        if data['notification_type2']:
            notification_type_tags.append('notification2')

        if data['notification_type3']:
            notification_type_tags.append('notification3') 
           
        userbinding = get_object_or_404(UserBindings, user=data['identity'])
        address = userbinding.address    
        try:
            service.bindings(userbinding.sid).delete()
        except:
            pass
        userbinding.delete()
        
        content = {
            "identity": data['identity'],
            "address": address,
            "binding_type": "fcm",
            "tag": notification_type_tags
        }
        binding = service.bindings.create(**content)
        body = {
            "user": data['identity'],
            "address":  address,
            "binding_type":  binding._properties['binding_type'],
            "sid": binding._properties['sid']
        }

        new_user_binding = UserBindings.objects.update_or_create(**body,defaults={"user": data['identity']})

        return Response({
            "success": True,
            "msg": "Notification Unsubuscribe successfully"
            })
