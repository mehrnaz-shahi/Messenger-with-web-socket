import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from main import models as main

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        pv_id = self.scope['url_route']['kwargs']['pv_id']

        pv = main.PV.objects.filter(id=pv_id)

        if pv:
            pv = pv[0]
            self.room_name = pv.id
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        pv_id = self.scope['url_route']['kwargs']['pv_id']

        pv = main.PV.objects.filter(id=pv_id)

        if pv:
            pv = pv[0]
            pvmessage = main.PVMessage(pv=pv, text=message, user=self.scope['user'])
            pvmessage.save()

        message = self.scope['user'].get_full_name() + ': ' + message
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
