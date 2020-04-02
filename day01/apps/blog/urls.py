#!/usr/bin/env python
#-*- coding:utf-8 -*-

from  django.conf.urls import url
from django.urls import path, include
from .views import *
from  rest_framework.routers import DefaultRouter
# 注册DRF
router = DefaultRouter()
router.register(r'bloglist', BlogListViewSet)

app_name = 'blog'

urlpatterns = [
    # drf
    path('', include(router.urls)),
    # blog
    path('base/', BlogView.as_view(), name='blog-base'),
    path('base/list/', BlogListView.as_view(), name='blog-base-list'),
    path('base/list2/', BlogListView2.as_view(), name='blog-base-list2'),
    path('base/create/', BlogCreateView.as_view(), name='blog-base-create'),
]
