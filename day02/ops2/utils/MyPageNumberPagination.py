from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response


class MyPagePagination(PageNumberPagination):
    """
    自定义分页
    """

    # 每页显示的个数
    page_size = 4
    # 可以动态改变每页显示的个数
    page_size_query_param = 'rows'
    # 页码参数
    page_query_param = 'page'
    max_page_size = None

    def get_paginated_response(self, data):
        code = 200
        msg = 'success'
        if not data:
            code = 404
            msg = "Data Not Found"

        return Response(OrderedDict([
            ('code', code),
            ('msg', msg),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data),
        ]))
