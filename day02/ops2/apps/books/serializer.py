from .models import Book, Publisher, Author
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class PublisherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='名称', max_length=32, min_length=2, required=True, help_text='名称',
                                 validators=[
                                     UniqueValidator(
                                         queryset=Publisher.objects.all(),
                                         message="出版社名称已存在"
                                     )],
                                 error_messages={
                                     "max_length": "最大32个字符",
                                     "min_length": "最少2个字符",
                                     'required':  '请输入出版社名称'
                                 })
    address = serializers.CharField(label='地址', max_length=32, min_length=2, required=True, help_text='地址',
                                    error_messages={
                                        "max_length": "最大32个字符",
                                        "min_length": "最少2个字符",
                                        "required": "地址不能为空"
                                    })
    city = serializers.CharField(label='城市', max_length=32, min_length=2, required=True, help_text='城市',
                                 error_messages={
                                     "max_length": "最大32个字符",
                                     "min_length": "最少2个字符",
                                     "required": "城市不能为空"
                                 })

    class Meta:
        model = Publisher
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
