#!/usr/bin/env python
# _#_ coding:utf-8 _*_
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.system.serializer import *
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from apps.system.forms import *
import re

class UserManageView(LoginRequiredMixin, APIView):
    login_url = '/login/'

    # @permission_required("apps.system.assets_read_user", "/403/")
    def get(self, request):

        return render(request, 'user_manage.html', locals())


class USerListView(APIView):

    def get(self, request):
        search_kw = request.GET.get('search_kw', None)
        # print('search:', search_kw)
        # 获取分页参数用于查询对应页面数据，page为第几页，num为每页数据条数,right_boundary为数据切片的右侧边界
        page = request.GET.get('page')
        num = request.GET.get('rows')
        right_boundary = int(page) * int(num)
        # print(page, num, int(page) * int(num))
        # 如果搜索关键字不为空，则根据此关键字模糊查询
        if search_kw:
            query = User.objects.filter(Q(username__contains=search_kw) | Q(email__contains=search_kw))[int(num) * (int(page) - 1):right_boundary]
            # 获取查询结果的总条数
            total = User.objects.filter(Q(username__contains=search_kw) | Q(email__contains=search_kw)).count()
            # print('11查询结果总数为:', total)
        else:
            # 根据前台传来的分页信息，页码（page）和每页条数（rows）,计算分页后的查询对象片段，例如前台传来第2页的参数，
            # rows=10，page=2，则服务端需要给前台返回[10:20]的数据片段，切片是左闭右开，所以最大只会取到下标为10到19，共10个数据
            query = User.objects.all()[int(num) * (int(page) - 1):right_boundary]
            total = User.objects.all().count()
            # print('22查询结果总数为:', total)
        ser = UserSerializer(query, many=True)
        row = ser.data
        return Response({'total': total, 'rows': row})


class UserCreateView(APIView):

    def get(self,  request):
        return render(request, 'user_create.html')

    def post(self, request):
        user_create_form = UserCreateForm(request.POST)
        if user_create_form.is_valid():
            new_user = user_create_form.save(commit=False)
            new_user.password = make_password(user_create_form.cleaned_data['password'])
            new_user.save()
            ret = {'status': 'success'}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_create_form.errors)
            user_create_form_errors = re.findall(pattern, errors)
            print(errors)
            ret = {
                'status': 'fail',
                'user_create_form_errors': user_create_form_errors[0]
            }

        return Response(ret)


class UserUpdateView(APIView):
    def get(self, request):
        user = get_object_or_404(User, pk=int(request.GET['id']))
        return render(request, 'user_update.html', locals())

    def post(self, request):
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User, pk=int(request.POST['id']))
        else:
            user = get_object_or_404(User, pk=int(request.user.id))
        user_update_form = UserUpdateForm(request.POST, instance=user)
        if user_update_form.is_valid():
            user_update_form.save()
            ret = {"status": "success"}
        else:

            ret = {"status": "fail", "message": user_update_form.errors}
        return Response(ret)
