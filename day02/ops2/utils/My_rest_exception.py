# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.views import exception_handler
import json

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        # print("res  data:", response.data)
        # print("response", response)
        # print(type(response.data))
        # print(str(response.data))
        from rest_framework.renderers import JSONRenderer
        jr = json.loads(str(JSONRenderer().render(response.data), encoding='utf-8'))

        response.data.clear()
        response.data['code'] = response.status_code

        try:
            response.data['data'] = {k: v[0] for k, v in jr.items()}
        except Exception as e:
            response.data['data'] = []

        if response.status_code == 404:
            try:
                response.data['message'] = response.data.pop('detail')
                response.data['message'] = "Not found"
            except KeyError:
                response.data['message'] = "Not found"

        if response.status_code == 400:
            response.data['message'] = 'Input error'

        elif response.status_code == 401:
            response.data['message'] = "Auth failed"

        elif response.status_code >= 500:
            response.data['message'] = "Internal service errors"

        elif response.status_code == 403:
            response.data['message'] = "Access denied"

        elif response.status_code == 405:
            response.data['message'] = 'Request method error'
        response.code = response.status_code
        response.status_code = 200
    # return Response({'data':  response.data})
    return Response(response.data)
