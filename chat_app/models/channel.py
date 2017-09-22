from django.db import models

from .abstract_date_time_model import AbstractDateTimeModel


class Channel(AbstractDateTimeModel):
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    created_by = models.IntegerField()

    def __unicode__(self):
        return unicode("%s" % self.name)

    @classmethod
    def create_channel(cls, name, user_id, is_public=True):
        channel = cls.objects.create(name=name, user_id=user_id, is_public=is_public)
        return channel

    @classmethod
    def join_channel(cls, channel_id, user_id):
        cls.get_channel_obj(channel_id)
        from chat_app.models.channel_member import ChannelMember
        ChannelMember.join_member(user_id, channel_id)

        from chat_app.utils.response_utils import http_response
        return http_response(200, "Successfully Joined")

    @classmethod
    def leave_channel(cls, channel_id, user_id):
        cls.get_channel_obj(channel_id)
        from chat_app.models.channel_member import ChannelMember
        ChannelMember.remove_member(user_id, channel_id)

        from chat_app.utils.response_utils import http_response
        return http_response(200, "Successfully Left")

    @classmethod
    def list_public_channels(cls):
        return list(cls.objects.filter(is_public=True).values())

    @classmethod
    def get_channel_obj(cls, channel_id):
        try:
            return cls.objects.get(id=channel_id)
        except cls.DoesNotExist:
            from chat_app.utils.response_utils import http_response
            return http_response(404, "Channel Not Found")

    @classmethod
    def get_channel_obj_after_checking_owner(cls, channel_id, user_id):
        channel_obj = cls.get_channel_obj(channel_id)
        if channel_obj.created_by == user_id:
            return channel_obj
        else:
            from chat_app.utils.response_utils import http_response
            return http_response(403, "You are not the Owner of this channel")

    @classmethod
    def delete_channel(cls, channel_id, user_id):
        channel_obj = cls.get_channel_obj_after_checking_owner(channel_id, user_id)
        channel_obj.delete()

        from chat_app.utils.response_utils import http_response
        return http_response(200, "Successfully deleted")

    @classmethod
    def update_channel(cls, channel_id, user_id, name, is_public):
        channel_obj = cls.get_channel_obj_after_checking_owner(channel_id, user_id)
        channel_obj.name = name
        channel_obj.is_public = is_public
        channel_obj.save()

        from chat_app.utils.response_utils import http_response
        return http_response(200, "Successfully updated")

    @classmethod
    def get_channel(cls, channel_id, user_id):
        channel_obj = cls.get_channel_obj(channel_id)

        from chat_app.models.channel_member import ChannelMember
        member_ids = ChannelMember.get_channel_members(channel_id)

        all_member_ids = [channel_obj.created_by]
        all_member_ids.extend(member_ids)

        from chat_app.utils.user_utils import get_users_dict
        users, users_dict = get_users_dict(all_member_ids)

        members = []
        for each_member_id in member_ids:
            members.append(users_dict[each_member_id])

        is_member = user_id in users_dict.keys()
        channel_dict = {
            "name": channel_obj.name,
            "is_public": channel_obj.is_public,
            "created_by": channel_obj.created_by,
            "creation_datetime": channel_obj.creation_datetime,
            "members": members,
            "is_member": is_member
        }
        return channel_dict
