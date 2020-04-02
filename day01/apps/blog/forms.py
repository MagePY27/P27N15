#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from .models import Blog


class BlogCreateFrom(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['name', 'tagline']

    error_message = {
        "name": {"required": "名称不能为空"},
        "tagline": {"required": "标签不能为空"}
    }
