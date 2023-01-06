import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from jalali_date import datetime2jalali

from main import models as main

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        pv_id = self.scope['url_route']['kwargs']['pv_id']

        pv = main.PV.objects.filter(id=pv_id)

        if pv:
            pv = pv[0]
            if self.scope['user'] in [pv.user1, pv.user2]:
                self.room_name = pv.id
                self.room_group_name = 'chat_%s' % self.room_name

                # Join room group
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )

                self.accept()
            else:
                self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        t = text_data_json['type']

        pv_id = self.scope['url_route']['kwargs']['pv_id']

        pv = main.PV.objects.filter(id=pv_id)

        if pv:
            pv = pv[0]

            if t == 'MESSAGE':
                message = text_data_json['message']
                pvmessage = main.PVMessage(pv=pv, text=message, user=self.scope['user'])
                pvmessage.save()

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'message_id': pvmessage.id,
                        'user_id': self.scope['user'].id,
                        'user_first_name': self.scope['user'].first_name,
                        'time': datetime2jalali(pvmessage.created).strftime('%H:%M')
                    }
                )
            
            elif t == 'DELETE':
                pvmessage = main.PVMessage.objects.filter(id = text_data_json['message_id'])[0]
                pvmessage.is_deleted = True
                pvmessage.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'delete_message',
                        'message_id': pvmessage.id,
                    }
                )


    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_id = event['user_id']
        user_first_name = event['user_first_name']
        message_id = event['message_id']
        time = event['time']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'MESSAGE',
            'message': message,
            'user_id': user_id,
            'user_first_name': user_first_name,
            'message_id': message_id,
            'time': time
        }))

    
    def delete_message(self, event):
        message_id = event['message_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'DELETE',
            'message_id': message_id,
        }))
