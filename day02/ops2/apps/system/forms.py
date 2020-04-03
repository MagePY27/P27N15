import re
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": "确认密码不能为空",
            "min_length": "密码长度最少6位数",
        }
    )

    class Meta:
        model = User
        fields = [
            'name', 'username', 'password', 'email', 'gender'
        ]

        error_messages = {
            "name": {"required": "姓名不能为空"},
            "username": {"required": "用户名不能为空"},
            "email": {"required": "邮箱不能为空"},
        }

    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if User.objects.filter(username=username).count():
            raise forms.ValidationError('用户名：{}已存在'.format(username))

        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")

        if User.objects.filter(email=email).count():
            raise forms.ValidationError('邮箱：{}已存在'.format(email))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'gender']


class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"密码不能为空"
        })

    confirm_password = forms.CharField(
        required=True,
        min_length=6,
        max_length=20,
        error_messages={
            "required": u"确认密码不能为空"
        })

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("两次密码输入不一致")
