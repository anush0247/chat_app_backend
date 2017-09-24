from django.db import models

from chat_app.models.channel import Channel
from .abstract_date_time_model import AbstractDateTimeModel


class ChannelMember(AbstractDateTimeModel):
    channel = models.ForeignKey(Channel, related_name="members")
    user_id = models.IntegerField()

    class Meta:
        unique_together = ('user_id', 'channel')

    def __unicode__(self):
        return unicode("%s-%s" % (self.channel_id, self.user_id))

    @classmethod
    def get_channel_members(cls, channel_id):
        return list(cls.objects.filter(channel_id=channel_id).values_list('user_id', flat=True))

    @classmethod
    def join_member(cls, user_id, channel_id):
        from chat_app.utils.response_utils import http_response
        from django.db import IntegrityError
        try:
            cls.objects.create(channel_id=channel_id, user_id=user_id)
            return http_response(200, "Successfully Joined")
        except IntegrityError:
            return http_response(400, "Already member in channel")

    @classmethod
    def member_channels(cls, user_id):
        return list(cls.objects.filter(user_id=user_id).values_list('channel_id', flat=True))

    @classmethod
    def remove_member(cls, user_id, channel_id):
        from chat_app.utils.response_utils import http_response
        try:
            cls.objects.get(channel_id=channel_id, user_id=user_id).delete()
            return http_response(200, "Successfully Left")
        except cls.DoesNotExist:
            return http_response(404, "Member not found")
