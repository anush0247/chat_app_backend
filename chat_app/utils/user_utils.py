def get_users_dict(user_ids):
    from django.contrib.auth import get_user_model
    user = get_user_model()
    users = user.objects.filter(id__in=user_ids).values()
    users_dict = dict()
    for each_user in users:
        each_user["user_id"] = each_user['id']
        users_dict[each_user['id']] = each_user
    return users, users_dict


def get_user_dict(user_obj):
    user_dict = {
        "username": user_obj.username,
        "first_name": user_obj.first_name,
        "last_name": user_obj.last_name,
        "email": user_obj.email,
        "user_id": user_obj.id,
    }
    return user_dict
