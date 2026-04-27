from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'teacher_approved']
    list_filter = ['role', 'teacher_approved']
    search_fields = ['user__username', 'user__email', 'preferred_name']