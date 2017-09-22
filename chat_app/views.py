from oauth2_provider.decorators import protected_resource
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@protected_resource(scopes=['read'])
def user_profile(request):
    user = request.user
    from chat_app.utils.user_utils import get_user_dict
    from chat_app.utils.response_utils import json_response
    return json_response(get_user_dict(user))


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@protected_resource(scopes=['read'])
def list_public_channels(request):
    from chat_app.models import Channel
    from chat_app.utils.response_utils import json_response
    return json_response(Channel.list_public_channels())
