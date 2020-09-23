import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Message, User, get_last_messages, not_routine

from django.shortcuts import get_object_or_404



class ChatConsumer(WebsocketConsumer):

    http_user_and_session = True

    def not_routine(self, author, to, url):
        not_routine(author, to, url)

    def fetch_messages(self, author, to):
        author, to = get_object_or_404(User, username=author), get_object_or_404(User, username=to)
        messages = get_last_messages(author, to)
        content = {
            'messages': self.messages_to_json(messages),
            'fetched': True,

        }
        self.send_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.author.username,
            'message': message.message,
            'time': str(message.time)
        }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        #self.fetch_messages(self.scope['url_route']['kwargs']['room_name'])

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def save_message(self, param):
        message = Message.objects.create(           
            author = get_object_or_404(User, username=param['author']),
            message = param['message'],
            to =  get_object_or_404(User, username=param['to'])
        )
        message.save()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get("command") == "fetch_messages":
            return self.fetch_messages( text_data_json.get("author"), text_data_json.get("to") )
        self.save_message(text_data_json)
        url = self.scope['server'][0] + ":" + str(self.scope['server'][1]) + "/chat/"+ self.scope['url_route']['kwargs']['room_name']
        self.not_routine(text_data_json.get("author"), text_data_json.get("to"), url)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': text_data_json['message'],
                'author': text_data_json['author'],   
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        #Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author': event['author'],
            'fetched': False,
        }))

    def send_message(self, message):
        self.send(text_data=json.dumps(message))