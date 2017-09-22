from django.conf.urls import url

from .views import list_public_channels

urlpatterns = [

    url(r'^channels/public/$', list_public_channels),
]

