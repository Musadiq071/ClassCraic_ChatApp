from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from deep_translator import GoogleTranslator

from .models import ChatGroup, GroupMessage
from .forms import ChatmessageCreateForm, JoinClassForm, CreateClassGroupForm


def is_group_teacher(user, group):
    return (
        group.teacher == user and
        user.profile.role == 'teacher' and
        user.profile.teacher_approved
    )


def can_manage_group(user, group):
    return user.is_staff or user.is_superuser or is_group_teacher(user, group)


def can_access_group(user, group):
    is_member = group.members.filter(id=user.id).exists()
    return can_manage_group(user, group) or is_member


@login_required
def chat_view(request):
    chat_group = get_object_or_404(
        ChatGroup,
        group_name='public-chat',
        chat_type='public'
    )

    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    online_count = chat_group.users_online.count()

    return render(request, 'rtchat/chat.html', {
        'chat_group': chat_group,
        'chat_messages': chat_messages,
        'form': form,
        'online_count':online_count,
    })


@login_required
def chatroom_view(request, group_name):
    chat_group = get_object_or_404(ChatGroup, group_name=group_name)

    if chat_group.chat_type == 'public':
        return redirect('home')

    if not can_access_group(request.user, chat_group):
        messages.warning(request, "You are not allowed to access this chat.")
        return redirect('home')

    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    other_user = None
    other_user_online = False
    online_count = chat_group.users_online.count()

    if chat_group.chat_type == 'private':
        other_user = chat_group.members.exclude(id=request.user.id).first()

        if other_user:
            other_user_online = chat_group.users_online.filter(id=other_user.id).exists()

    return render(request, 'rtchat/chat.html', {
        'chat_group': chat_group,
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'other_user_online': other_user_online,
        'online_count': online_count,
    })


@login_required
def create_class_group(request):
    profile = request.user.profile

    if not (profile.role == 'teacher' and profile.teacher_approved):
        messages.warning(request, "Only approved teachers can create class groups.")
        return redirect('home')

    form = CreateClassGroupForm()

    if request.method == 'POST':
        form = CreateClassGroupForm(request.POST)

        if form.is_valid():
            group = form.save(commit=False)
            group.chat_type = 'class'
            group.teacher = request.user
            group.save()
            group.members.add(request.user)

            messages.success(request, f"Class created! Code: {group.join_code}")
            return redirect('chatroom', group_name=group.group_name)

    return render(request, 'rtchat/create_group.html', {
        'form': form
    })


@login_required
def join_class_group(request):
    form = JoinClassForm()

    if request.method == 'POST':
        form = JoinClassForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data['code']

            try:
                group = ChatGroup.objects.get(join_code=code, chat_type='class')
            except ChatGroup.DoesNotExist:
                messages.error(request, "Invalid class code.")
            else:
                group.members.add(request.user)
                messages.success(request, "Joined class successfully!")
                return redirect('chatroom', group_name=group.group_name)

    return render(request, 'rtchat/join_group.html', {
        'form': form
    })


@login_required
def start_private_chat(request, username):
    other_user = get_object_or_404(User, username=username)

    if other_user == request.user:
        messages.warning(request, "You cannot start a chat with yourself.")
        return redirect('home')

    # fixed name avoids duplicate private chats
    user1_id = min(request.user.id, other_user.id)
    user2_id = max(request.user.id, other_user.id)
    group_name = f"pm-{user1_id}-{user2_id}"

    private_chat, created = ChatGroup.objects.get_or_create(
        group_name=group_name,
        defaults={'chat_type': 'private'}
    )

    if private_chat.chat_type != 'private':
        messages.error(request, "A group with this name already exists and is not private.")
        return redirect('home')

    private_chat.members.add(request.user, other_user)

    return redirect('chatroom', group_name=private_chat.group_name)


@login_required
def chat_attachment_upload(request, group_name):
    chat_group = get_object_or_404(ChatGroup, group_name=group_name)

    # check permission before upload
    if chat_group.chat_type != 'public' and not can_access_group(request.user, chat_group):
        messages.warning(request, "You are not allowed to upload files to this chat.")
        return redirect('home')

    form = ChatmessageCreateForm(request.POST, request.FILES)

    if form.is_valid():
        message = form.save(commit=False)
        message.author = request.user
        message.group = chat_group
        message.save()

        channel_layer = get_channel_layer()
        room_group_name = f'chat_{chat_group.id}'

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'message_handler',
                'message_id': message.id,
            }
        )

        return HttpResponse()

    return render(request, "rtchat/partials/upload_error.html", {
        "form": form
    })


@login_required
def start_chat_list_view(request):
    users = (
        User.objects
        .exclude(id=request.user.id)
        .select_related('profile')
        .order_by('username')
    )

    return render(request, 'rtchat/start_chat_list.html', {
        'users': users,
    })


@login_required
def leave_chat(request, group_name):
    chat_group = get_object_or_404(ChatGroup, group_name=group_name)

    if chat_group.chat_type not in ['class', 'private']:
        messages.warning(request, "You cannot leave this chat.")
        return redirect('home')

    if chat_group.members.filter(id=request.user.id).exists():
        chat_group.members.remove(request.user)
        messages.success(request, "You left the chat.")

    return redirect('home')


@login_required
def manage_group_view(request, group_name):
    group = get_object_or_404(ChatGroup, group_name=group_name)

    if not can_manage_group(request.user, group):
        messages.warning(request, "You are not allowed to manage this group.")
        return redirect('home')

    return render(request, 'rtchat/manage_group.html', {
        'group': group
    })


@login_required
@require_POST
def remove_group_member(request, group_name, username):
    group = get_object_or_404(ChatGroup, group_name=group_name)

    if not can_manage_group(request.user, group):
        return redirect('home')

    user_to_remove = get_object_or_404(User, username=username)

    if user_to_remove == group.teacher:
        messages.warning(request, "You cannot remove the group owner.")
        return redirect('manage-group', group_name=group.group_name)

    group.members.remove(user_to_remove)
    messages.success(request, "Member removed.")

    return redirect('manage-group', group_name=group.group_name)


@login_required
@require_POST
def delete_group(request, group_name):
    group = get_object_or_404(ChatGroup, group_name=group_name, chat_type='class')

    if not can_manage_group(request.user, group):
        messages.warning(request, "You are not allowed to delete this group.")
        return redirect('home')

    group.delete()
    messages.success(request, "Group deleted successfully.")

    return redirect('home')


@login_required
#Translate message feature
def translate_message(request, message_id):
    message = get_object_or_404(GroupMessage, id=message_id)

    # check if user can access translated message
    if message.group.chat_type != 'public' and not can_access_group(request.user, message.group):
        return HttpResponse("Not allowed", status=403)

    try:
        translated_text = GoogleTranslator(
            source='auto',
            target='en'
        ).translate(message.body)

    except Exception:
        translated_text = "Translation unavailable right now."

    return render(request, "rtchat/partials/translated_message.html", {
        "translated_text": translated_text
    })