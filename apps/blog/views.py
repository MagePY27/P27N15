import json
import re

from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic.base import View
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import filters
from utils.MyPageNumberPagination import MyPageination, MyLimitMyPageination


class BlogListViewSet(mixins.ListModelMixin,  viewsets.GenericViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializers
    # 分页
    pagination_class = MyPageination
    # filter 后台
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filter
    filter_fields = ['name', 'tagline']
    # 搜索
    search_fields = ('name', 'tagline')


class BlogListView(View):
    def get(self, request):
        print("==="*20)
        print("dict:", QueryDict(request.body).dict())
        search_kw = request.GET.get('search_kw', None)
        print('search:', search_kw)
        # 获取分页参数用于查询对应页面数据，page为第几页，num为每页数据条数,right_boundary为数据切片的右侧边界
        page = request.GET.get('page')
        num = request.GET.get('rows')
        right_boundary = int(page)*int(num)
        print(page, num, int(page)*int(num))
        # 如果搜索关键字不为空，则根据此关键字模糊查询blog的name和tabline
        if search_kw:
            blog_query = Blog.objects.filter(Q(name__contains=search_kw) | Q(tagline__contains=search_kw))[
                        int(num) * (int(page) - 1):right_boundary]
            # 获取查询结果的总条数
            total = Blog.objects.filter(Q(name__contains=search_kw) | Q(tagline__contains=search_kw)).count()
            print('11查询结果总数为:', total)
        else:
            # 根据前台传来的分页信息，页码（page）和每页条数（rows）,计算分页后的blog对象片段，例如前台传来第2页的参数，
            # rows=10，page=2，则服务端需要给前台返回[10:20]的数据片段，切片是左闭右开，所以最大只会取到下标为10到19，共10个数据
            blog_query = Blog.objects.all()[int(num) * (int(page) - 1):right_boundary]
            # server端分页时必须返回total和rows,total用于分页时显示总数
            total = Blog.objects.all().count()
            print('22查询结果总数为:', total)
        # rows为具体数据
        rows = []
        # 遍历查询出的user对象，将对应数据放到rows中
        for item in blog_query:
            rows.append({'id': item.id, 'name': item.name, 'tagline': item.tagline})
        print(rows)
        # return render(request, 'account/user_management.html', {'rows': json.dumps(rows, cls=DateEncoder)})
        # 序列化数据，因为有datetime类型数据，所以使用自定义类DateEncoder序列化
        return HttpResponse(json.dumps({'total': total, 'rows': rows}))


# class BlogListView(APIView):
#
#     def get(self, request):
#         print("body:========", request.body)
#         print("dict:", QueryDict(request.body).dict())
#         # print(request.body)
#         # pageSize = int(request.GET.get('pageSize'))
#         # pageNumber = int(request.GET.get('pageNumber'))
#         # searchText = request.GET.get('searchText')
#         # sortName = request.GET.get('sortName')
#         # sortOrder = request.GET.get('sortOrder')
#         #
#         # print("size", pageSize)
#         # print("Number", pageNumber)
#         # print("search", searchText)
#         # print("sortName", sortName)
#         # print("sortOrder", sortOrder)
#
#         # 获取所有数据
#         queryset = Blog.objects.all()
#         # 分页
#         pg = MyPageination()
#         # 在数据库中获取纷纷也数据
#         pager_roles = pg.paginate_queryset(queryset=queryset, request=request, view=self)
#         # 对纷纷也数据进行序列化
#         ser = BlogModelSerializers(instance=pager_roles,  many=True)
#         print(ser.data)
#         # return pg.get_paginated_response(ser.data)
#         return Response(ser.data)


class BlogListView2(APIView):
    def get(self, request):
        blog_list = Blog.objects.all()

        paginator = MyLimitMyPageination()
        page_blog_list = paginator.paginate_queryset(blog_list, self.request, view=self)

        ser = BlogModelSerializers(page_blog_list, many=True)
        res = paginator.get_paginated_response(ser.data)
        return res


class BlogView(APIView):
    """
    blog总表
    """
    def get(self, requesst):
        return render(requesst, 'blog/blog.html', locals())


class BlogCreateView(APIView):
    """
    blog 新增
    """
    def get(self, request):
        ret = dict(blog_list=Blog.objects.all())
        if 'id' in request.GET and request.GET['id']:
            blog = get_object_or_404(Blog,  pk=request.GET['id'])
            ret['blog'] = blog
        return render(request, 'blog/blog_create.html', ret)

    def post(self, request):
        print("-----------create-----------")
        from .forms import BlogCreateFrom
        create_form = BlogCreateFrom(request.POST)
        if create_form.is_valid():
            new_form = create_form.save(commit=False)
            new_form.save()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(create_form.errors)
            create_form_errors = re.findall(pattern, errors)
            ret = {
                'status': 'fail',
                'idc_create_form_errors': create_form_errors[0]
            }
        return HttpResponse(json.dumps(ret), content_type='application/json')
        # return Response(ret)

