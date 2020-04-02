from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    name = models.CharField(max_length=20, default="", verbose_name="姓名")
    gender = models.IntegerField(choices=((0, "男"), (1, "女")), default=0, verbose_name="性别")
    email = models.EmailField(max_length=50, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


