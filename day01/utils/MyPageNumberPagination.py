#!/usr/bin/env python
#-*- coding:utf-8 -*-

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class MyPageination(PageNumberPagination):
    """
    自定义分页设置
    """
    # 默认每页显示的个数
    page_size = 1
    # 可以动态改变每页显示的个数
    page_size_query_param = 'size'
    # 页码参数
    page_query_param = 'draw'
    # 最多能显示多少页
    max_page_size = 100


class MyLimitMyPageination(LimitOffsetPagination):
    # 默认每页显示的数据条数
    default_limit = 1
    # URL中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # URL中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显得条数
    max_limit = None
