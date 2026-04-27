from django.contrib import admin
from .models import *

# Registered models 
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)