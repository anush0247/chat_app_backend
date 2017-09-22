from django.conf.urls import url

from .views import list_public_channels
from .views import user_profile

chat_urlpatterns = [

    url(r'^/channels/public/$', list_public_channels),
]

user_urlpatterns = [
    url(r'^/profile/$', user_profile),
]
