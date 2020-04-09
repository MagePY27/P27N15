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
                                     'required': '请输入出版社名称'
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


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label='姓名', max_length=32, min_length=2, required=True, help_text='姓名',
                                 validators=[
                                     UniqueValidator(
                                         queryset=Author.objects.all(),
                                         message="作者姓名已存在"
                                     )],
                                 error_messages={
                                     "max_length": "最大32个字符",
                                     "min_length": "最少2个字符",
                                     'required': '请输入作者名称'
                                 })
    email = serializers.CharField(label='邮箱', required=True, help_text='邮箱',
                                  error_messages={
                                      "required": "邮箱不能为空"
                                  })

    class Meta:
        model = Author
        fields = "__all__"


class AuthorDisplaySerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "name"


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(label='书名', required=True, help_text='书名',
                                  error_messages={"required": "书名不能为空"
                                                  })
    # 显示外键
    publisher = serializers.CharField(source='publisher.name', read_only=True)
    # many to many
    # authors = AuthorSerializer(many=True, read_only=True)
    authors = serializers.StringRelatedField(many=True, read_only=True)
    # authors = AuthorDisplaySerializers(many=True, read_only=True)

    class Meta:
        model = Book
        # fields = ['id', 'title', 'publisher']
        fields = ['id', 'title', 'publisher', 'authors']

