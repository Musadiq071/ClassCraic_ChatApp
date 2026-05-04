from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.exceptions import ValidationError

class ChatGroup(models.Model):
    CHAT_TYPE_CHOICES = (
        ('public', 'Public'),
        ('class', 'Class'),
        ('private', 'Private')
    )

    group_name = models.CharField(max_length=120, unique=True)
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPE_CHOICES, default='public')

    #used to join chat_group by students 
    join_code = models.CharField(max_length=12, unique=True, blank=True, null=True)

    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)

    teacher = models.ForeignKey(
        User,on_delete=models.SET_NULL, null=True, blank=True,related_name='created_chat_groups')

    members = models.ManyToManyField(
        User,
        related_name='joined_chat_groups',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.chat_type == 'class' and not self.join_code:
            self.join_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.group_name
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        #allow message text, file or both 
        body = (self.body or '').strip()
        if not body and not self.file:
            raise ValidationError("Message must contain text or an attachment.")

    def save(self, *args, **kwargs):
        if self.body:
            self.body = self.body.strip()
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.body:
            return f'{self.author.username} : {self.body}'
        if self.file:
            return f'{self.author.username} uploaded a file'
        return f'Message by {self.author.username}'

    class Meta:
        ordering = ['-created']