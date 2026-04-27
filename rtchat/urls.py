from django.urls import path
from .views import *

urlpatterns = [
    #Public Chat
    path('chat/public/', chat_view, name='public-chat'),

    # Private chat URLs for creating and managing
    path('chat/start/', start_chat_list_view, name='start-chat-list'),
    path('chat/start/<str:username>/', start_private_chat, name='start-private-chat'),
    path('chat/leave/<str:group_name>/', leave_chat, name='leave-chat'),
    #Group managemnt only for teachers/admin
    path('chat/<str:group_name>/manage/', manage_group_view, name='manage-group'),
    path('chat/<str:group_name>/remove/<str:username>/', remove_group_member, name='remove-group-member'),
    path('chat/<str:group_name>/delete/', delete_group, name='delete-group'),
    # GENERIC CHAT ROOM 
    path('chat/<str:group_name>/', chatroom_view, name='chatroom'),

    #Class Group actions for teachers and students
    path('create-group/', create_class_group, name='create-group'),
    path('join-group/', join_class_group, name='join-group'),

    #File upload 
    path('chat/attachment_upload/<group_name>/', chat_attachment_upload, name="chat-attachment-upload"),
]