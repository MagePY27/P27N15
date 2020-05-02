from django.db import models


class Assets(models.Model):
    assets_type_choices = (
                          ('server', u'服务器'),
                          ('vmser', u'虚拟机'),
                          ('switch', u'交换机'),
                          )

    assets_type = models.CharField(choices=assets_type_choices, max_length=100, default='server', verbose_name='资产类型')
    ip = models.GenericIPAddressField(u'IP', blank=True, null=True)

    class Meta:
        verbose_name = "主机管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.ip)
