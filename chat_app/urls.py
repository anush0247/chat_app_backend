from django.conf.urls import url

from .views import list_public_channels
from .views import get_channel
from .views import get_channel_messages
from .views import join_channel



urlpatterns = [

    url(r'^channels/public/$', list_public_channels),
    url(r'^channels/public/(?P<channel_id>\d+)/$', get_channel),
    url(r'^channels/public/(?P<channel_id>\d+)/messages/$', get_channel_messages),
    url(r'^channels/public/(?P<channel_id>\d+)/join/$', join_channel),
]

