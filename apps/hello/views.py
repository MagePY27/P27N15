from django.shortcuts import render, HttpResponse
from django.views.generic.base import View, TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse, QueryDict


class HelloView(APIView):
    def get(self, request, **kwargs):
        year = kwargs.get('year')
        month = kwargs.get('month')

        return Response({'year': year, 'month': month})

    def post(self,  requst):
        print("method:", requst.method)
        print("body:",  requst.body)
        print("post:",  requst.POST)
        print("dict:",  QueryDict(requst.body).dict())

        return Response('post')


class IndexView(TemplateView):
    template_name = 'hello/index.html'


class HelloListView(APIView):

    def get(self, request):
        user = request.user.username
        ret = [
            {'name':  'aa',  'cn': 'sh', 'age':  11},
            {'name':  'aa',  'cn': 'sh', 'age':  12},
            {'name':  'aa',  'cn': 'bj', 'age':  13},
        ]
        return Response(ret)




