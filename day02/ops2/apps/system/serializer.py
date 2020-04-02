from rest_framework import serializers
from apps.system.models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'gender', 'email']

