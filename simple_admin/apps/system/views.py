from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.generic import View
from apps.system.forms import LoginForm


class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'base_index.html')


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        redirect_to = request.GET.get('next', '/')
        if login_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = auth.authenticate(username=username, password=password)
            print('=='*20, user)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                msg = '用户名或密码错误！！'
        else:
            msg = '用户名密码不能为空'
        return render(request, 'login.html', locals())


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')




