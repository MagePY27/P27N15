#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# 配置
# router.register(r'hello', )

app_name = 'hello'

urlpatterns = [
    # path('', include(router.urls)),
    path('', IndexView.as_view(), name='index'),
    path('hello/', IndexView.as_view(), name='hello-index'),
]
