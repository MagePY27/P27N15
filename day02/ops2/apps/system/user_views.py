from django.http import QueryDict

from .serializer import UserUpdateSerializer, UserSerializer
from rest_framework import viewsets
from apps.system.models import UserProfile
from django.contrib.auth import get_user_model

import json


class ReturnMsg:
    def __init__(self, code=1, msg='success', errors=None, data=None):
        self.code = code
        self.msg = msg
        self.errors = {} if errors is None else errors
        self.data = [] if data is None else data


class CustomModelViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'code':1})

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        print(response.data)
        return Response({'data': response.data, 'status': response.status_code})





class UserViewSetMixin(APIView, viewsets.ViewSetMixin):

    def post(self, request):
        print(request.data)

        pass