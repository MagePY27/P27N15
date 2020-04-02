#!/usr/bin/env python
#-*- coding:utf-8 -*-
from .models import Blog, Author, Entry
from rest_framework import serializers


class BlogModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class AuthorModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
