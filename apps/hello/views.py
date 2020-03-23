from django.shortcuts import render, HttpResponse

# Create your views here.
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework.views import APIView


class IndexView(APIView):
    def get(self, request):
        return Response('hello Django')


