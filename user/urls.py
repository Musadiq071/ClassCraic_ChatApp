from django.urls import path 
from user.views import *

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', profile_edit_view, name='profile-edit'),
    path('onboarding/', profile_edit_view, name='profile-onboarding'),
    path('settings/', profile_settings_view, name='profile-settings'),
    path('email_change', profile_emailchange, name="profile-emailchange"),
    path('emailverify/',profile_emailverify, name='profile-emailverify' ),
    path('delete/', profile_delete_view, name="profile-delete"),

    path('teachers/approvals/', teacher_approval_list, name='teacher-approval-list'),
    path('teachers/approve/<str:username>/', approve_teacher, name='approve-teacher'),
    path('teachers/disapprove/<str:username>/', disapprove_teacher, name='disapprove-teacher'),

    
    
]  
