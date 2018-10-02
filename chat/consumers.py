from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import User,Chatroom
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print(type(self.room_name))
        try:
            room=Chatroom.objects.get(name=self.room_name)
            room.no_of_users+=1
            room.save()
        except:
            pass
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
        user=text_data_json['user']
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user=event['user']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user':user,
        }))
