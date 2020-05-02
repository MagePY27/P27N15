# Generated by Django 2.2 on 2020-04-11 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assets_type', models.CharField(choices=[('server', '服务器'), ('vmser', '虚拟机'), ('switch', '交换机')], default='server', max_length=100, verbose_name='资产类型')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP')),
            ],
            options={
                'verbose_name': '主机管理',
                'verbose_name_plural': '主机管理',
            },
        ),
    ]
