from rest_framework import serializers
from apps.system.models import UserProfile
from django.contrib.auth.hashers import make_password, check_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'gender', 'email']


# from rest_framework.validators import
from rest_framework.validators import UniqueValidator


# 创建
class UserCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='姓名', max_length=32, min_length=4, help_text='姓名',
                                 validators=[
                                     UniqueValidator(
                                         queryset=UserProfile.objects.all(),
                                         message="姓名已存在"
                                     )],
                                 error_messages={
                                     "max_length": "最大32个字符",
                                     "min_length": "最少4个字符",
                                 })
    username = serializers.CharField(label='用户名', max_length=32, min_length=4, help_text='用户名',
                                     validators=[
                                         UniqueValidator(
                                             queryset=UserProfile.objects.all(),
                                             message="用户名已存在"
                                         )],
                                     error_messages={
                                         "max_length": "最大32个字符",
                                         "min_length": "最少4个字符",
                                     })
    password = serializers.CharField(label="密码", min_length=6, help_text="密码",)
    email = serializers.EmailField(label='mail', max_length=128, help_text='mail',)

    class Meta:
        model = UserProfile
        fields = ['name', 'username', 'gender', 'email', 'password']


class UserUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=20, label='姓名',
                                 validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="姓名")])
    username = serializers.CharField(required=True, allow_blank=False, max_length=20, label='用户名',
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message="用户名已存在")])

    # 这里的style把密码设置为密文的, 就像input标签type属性设置为password一样
    password = serializers.CharField(
        style={'input_type': 'password'}, label="密码", write_only=True, min_length=6,
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        校验所有的字段
        :param attrs:  attrs是所有字段组成的字典
        :return: attrs
        """
        print("==="*20, attrs)
        password = attrs['password']
        confirm_password = attrs['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError('两次密码不一样')

        return attrs

    def create(self, validated_data):
        del validated_data['confirm_password']
        user = super(UserUpdateSerializer, self).create(validated_data=validated_data)
        # 对密码加密
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = UserProfile
        fields = ['name', 'username', 'gender', 'email', 'password']