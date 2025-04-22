from rest_framework.response import Response


def response(status, message, data):
    data = {
        'status' : status,
        'message' : message,
        'data' : data
    }
    return Response(status = status, body = data, headers = {'Cache-Control':'no-cache'})