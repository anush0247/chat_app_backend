from django.db import models

from chat_app.models.channel import Channel
from .abstract_date_time_model import AbstractDateTimeModel


class ChannelMessage(AbstractDateTimeModel):
    channel = models.ForeignKey(Channel, related_name="messages")
    user_id = models.IntegerField()
    message = models.TextField()

    def __unicode__(self):
        return unicode("%s-%s-%s" % (self.channel_id, self.user_id, self.message))

    @classmethod
    def get_channel_message(cls, channel_id):
        return list(cls.objects.filter(channel_id=channel_id).order_by("-creation_datetime").values())

    @classmethod
    def add_channel_message(cls, user_id, message, channel_id):
        return cls.objects.create(user_id=user_id, channel_id=channel_id, message=message)

    @classmethod
    def get_message_obj(cls, message_id):
        try:
            return cls.objects.get(id=message_id)
        except cls.DoesNotExist:
            from chat_app.utils.response_utils import http_response
            return http_response(404, "Message not found")

    @classmethod
    def get_message_obj_after_checking_owner(cls, message_id, user_id):
        message_obj = cls.get_message_obj(message_id)
        if message_obj.created_by == user_id:
            return message_obj
        else:
            from chat_app.utils.response_utils import http_response
            return http_response(403, "You are not the Owner of this message")

    @classmethod
    def delete_message(cls, message_id, user_id):
        message_obj = cls.get_message_obj_after_checking_owner(message_id, user_id)
        message_obj.delete()

        from chat_app.utils.response_utils import http_response
        return http_response(200, "Successfully deleted")

    @classmethod
    def update_message(cls, message_id, user_id, message):
        message_obj = cls.get_message_obj_after_checking_owner(message_id, user_id)
        message_obj.message = message
        message_obj.save()

        from chat_app.utils.response_utils import http_response
        return http_response(200, "Successfully updated")
