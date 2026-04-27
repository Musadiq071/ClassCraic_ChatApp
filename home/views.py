from django.shortcuts import render
from rtchat.models import ChatGroup


#Displays homepage with public chats, class-group chats, private chats 
def home_view(request):
    
    
    public_chat = ChatGroup.objects.filter(chat_type='public').first()

    profile = None
    class_groups = ChatGroup.objects.none()
    created_groups = ChatGroup.objects.none()
    private_chats = []

    if request.user.is_authenticated:
        profile = request.user.profile

        #groups user has joined as a member
        class_groups = request.user.joined_chat_groups.filter(chat_type='class')
        #class groups created by user with teacher role 
        created_groups = request.user.created_chat_groups.filter(chat_type='class')
        #Private chats are stored as chatgroups with two members.
        private_groups = request.user.joined_chat_groups.filter(chat_type='private')

        for group in private_groups:
            other_user = group.members.exclude(id=request.user.id).first()
            last_message = group.chat_messages.first()
            
            if other_user:
                private_chats.append({
                    'group': group,
                    'other_user': other_user,
                    'last_message':last_message,
                })

    context = {
        'public_chat': public_chat,
        'class_groups': class_groups,
        'private_chats': private_chats,
        'created_groups': created_groups,
        'profile': profile,
    }

    return render(request, 'home.html', context)