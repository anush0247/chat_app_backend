# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from chat_app.models import ChannelMember, Channel, ChannelMessage

# Register your models here.

admin.site.register(ChannelMember)
admin.site.register(Channel)
admin.site.register(ChannelMessage)
