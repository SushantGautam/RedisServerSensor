import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "BoothMasterSocket"
        self.room_group_name = 'booth_updates'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': "refreshall",
                'boothname': "boothmaster",

            }
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, ):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        boothname = text_data_json['boothname']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'boothname': boothname,

            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        boothname = event['boothname']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'boothname': boothname,
            'ifsuccess': 'success',
        }))
