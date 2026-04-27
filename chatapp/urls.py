from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home.views import home_view
from user.views import profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

    path('', home_view, name='home'),
    path('', include('rtchat.urls')),

    path('profile/', include('user.urls')),
    path('@<username>/', profile_view, name='profile'),
]

# Only used in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)