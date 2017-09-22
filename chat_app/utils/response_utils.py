import json


def http_response(code, message):
    content = {
        "message": message
    }
    from django.http import HttpResponse
    return HttpResponse(status=code, content=json.dumps(content))


def json_response(response_dict):
    from django.http import HttpResponse
    return HttpResponse(status=200, content=json.dumps(response_dict), content_type="application/json")
