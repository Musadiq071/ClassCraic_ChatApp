from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher','Teacher'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE )
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    preferred_name = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    teacher_approved = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.user)
    
    
    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static('images/avatar.svg')
        return avatar