import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.utils import timezone

from jalali_date import datetime2jalali

from main import models as main

class GroupConsumer(WebsocketConsumer):
    def connect(self):
        group_id = self.scope['url_route']['kwargs']['group_id']

        group = main.Group.objects.filter(id=group_id)

        if group:
            group = group[0]
            self.room_name = group.id
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

        group_id = self.scope['url_route']['kwargs']['group_id']

        group = main.Group.objects.filter(id=group_id)
        if group:
            group = group[0]

            group_member = main.GroupMember.objects.filter(user = self.scope['user'], group=group, is_member=True)

            if t == 'MESSAGE':
                if not group_member:
                    return
            
                group_member = group_member[0]
                message = text_data_json['message']
                gpmessage = main.GroupMessage(group_member=group_member, text=message)
                gpmessage.save()

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'message_id': gpmessage.id,
                        'user_id': self.scope['user'].id,
                        'user_first_name': self.scope['user'].first_name,
                        'time': datetime2jalali(gpmessage.created).strftime('%H:%M')
                    }
                )
            
            elif t == 'REQUEST':
                
                action = text_data_json['action']

                if action == 'leave':
                    group_member = main.GroupMember.objects.filter(user = self.scope['user'], group=group, is_member=True)
                    if not group_member:
                        return

                    group_member = group_member[0]
                    group_member.is_member = False
                    group_member.leave_date = timezone.now()
                    group_member.save()

                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'success',
                        }
                    )
                elif action == 'add':
                    group_member = main.GroupMember.objects.filter(user = self.scope['user'], group=group, is_member=True)
                    if not group_member:
                        group_member = main.GroupMember(user=self.scope['user'], group=group, is_member=True)
                        group_member.save()
                    
                    
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'success',
                        }
                    )
            
            elif t == 'ADMIN':
                if group.owner != self.scope['user']:
                    return 
                
                username = text_data_json['username']

                group_member = main.GroupMember.objects.filter(user__username=username, group=group, is_member=True)

                if not group_member:
                    return
                
                group_member = group_member[0]
                group_member.is_admin = not group_member.is_admin
                group_member.save()

                async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'success',
                        }
                    )
            
            elif t == 'DELETE':
                if not group_member:
                    return
            
                gpmessage = main.GroupMessage.objects.filter(id = text_data_json['message_id'])[0]

                if gpmessage.group_member.user != self.scope['user']:
                    return

                gpmessage.is_deleted = True
                gpmessage.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'delete_message',
                        'message_id': gpmessage.id,
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

    
    def success(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'REQUEST',
            'success': True,
        }))


    def delete_message(self, event):
        message_id = event['message_id']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'DELETE',
            'message_id': message_id,
        }))

    
