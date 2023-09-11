import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from chat.models import User

# A dictionary to keep track of WebSocket connections for each group_name
connected_users = {}


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']

        if self.user.is_authenticated:
            # Add the WebSocket connection to the user's group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            # Store the user's WebSocket connection
            connected_users[self.user.username] = self.channel_name

            self.accept()
        else:
            # Reject the connection if the user is not authenticated
            self.close()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            # Remove the WebSocket connection from the user's group
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

            # Remove the user's WebSocket connection from the dictionary
            del connected_users[self.user.username]

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        group_name = text_data_json['roomName']  # Get the group_name from the frontend

        if self.user.is_authenticated:
            if group_name == "All":
                # Send the message to all connected users
                for username, channel_name in connected_users.items():
                    if username != self.user.username:
                        async_to_sync(self.channel_layer.send)(
                            channel_name,
                            {
                                'type': 'chat_message',
                                'message': message,
                                'sender_username': self.user.username
                            }
                        )
            else:
                # Find users who belong to the same group_name as provided from the frontend
                users_in_same_group = User.objects.filter(group_name=group_name)
                for user in users_in_same_group:
                    # Check if the user is connected
                    if user.username in connected_users and user.username != self.user.username:
                        # Send the message to connected users in the same group
                        async_to_sync(self.channel_layer.send)(
                            connected_users[user.username],
                            {
                                'type': 'chat_message',
                                'message': message,
                                'sender_username': self.user.username
                            }
                        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message
        }))
