import datetime
import json


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return str(x)
    return x


def http_response(code, message):
    content = {
        "message": message
    }
    from django.http import HttpResponse
    return HttpResponse(status=code, content=json.dumps(content), default=datetime_handler)


def json_response(response_dict):
    from django.http import HttpResponse
    return HttpResponse(status=200, content=json.dumps(response_dict, default=datetime_handler),
                        content_type="application/json")
