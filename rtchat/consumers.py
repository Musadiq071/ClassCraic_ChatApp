from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from asgiref.sync import async_to_sync
from .models import ChatGroup, GroupMessage
import json


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)

        # Use unique database id for group name
        self.room_group_name = f"chat_{self.chatroom.id}"

        # logged-In users can only open websocket connection
        if not self.user.is_authenticated:
            self.close()
            return

        # Permission for class and private chats
        if self.chatroom.chat_type in ['class', 'private']:
            is_admin = self.user.is_staff or self.user.is_superuser
            is_teacher_owner = (
                self.chatroom.teacher == self.user and
                self.user.profile.role == 'teacher' and
                self.user.profile.teacher_approved
            )
            is_member = self.chatroom.members.filter(id=self.user.id).exists()

            if not (is_admin or is_teacher_owner or is_member):
                self.close()
                return

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if not self.chatroom.users_online.filter(id=self.user.id).exists():
            self.chatroom.users_online.add(self.user)
            self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'chatroom'):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

            #Remove the user from online list when socket conection closes
            if self.user.is_authenticated:
                if self.chatroom.users_online.filter(id=self.user.id).exists():
                    self.chatroom.users_online.remove(self.user)
                    self.update_online_count()

    def receive(self, text_data):
        if not self.user.is_authenticated:
            return
        #Check permissions before message is saved
        if self.chatroom.chat_type in ['class', 'private']:
            is_admin = self.user.is_staff or self.user.is_superuser
            is_teacher_owner = (
                self.chatroom.teacher == self.user and
                self.user.profile.role == 'teacher' and
                self.user.profile.teacher_approved
            )
            is_member = self.chatroom.members.filter(id=self.user.id).exists()

            if not (is_admin or is_teacher_owner or is_member):
                return

        text_data_json = json.loads(text_data)
        body = text_data_json.get('body', '').strip()
        
        #empty message  is not saved
        if not body:
            return

        message = GroupMessage.objects.create(
            body=body,
            author=self.user,
            group=self.chatroom
        )

        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            event
        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)

        context = {
            'message': message,
            'user': self.user,
        }

        html = render_to_string(
            "rtchat/partials/chat_message_p.html",
            context=context
        )
        self.send(text_data=html)

    def update_online_count(self):
        online_count = self.chatroom.users_online.count()

        event = {
            'type': 'online_count_handler',
            'online_count': online_count,
        }

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            event
        )

    def online_count_handler(self, event):
        online_count = event['online_count']
        html = render_to_string(
            "rtchat/partials/online_count.html",
            {'online_count': online_count}
        )
        self.send(text_data=html)