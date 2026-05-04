from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from home.views import home_view, about_view
from user.views import profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    #auth(login,signup, passwordreset etc)
    path('accounts/', include('allauth.urls')),
    #main pages
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    #chat routes(public,private,class_groups)
    path('', include('rtchat.urls')),
    #user profiles
    path('profile/', include('user.urls')),
    path('@<username>/', profile_view, name='profile'),
    #serves media file(only for development)
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT
    }),
]