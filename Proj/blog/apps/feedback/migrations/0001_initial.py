# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email', models.CharField(verbose_name='留言用户邮箱', max_length=30)),
                ('content', models.TextField(verbose_name='留言内容', blank=True, null=True)),
                ('pub_date', models.DateTimeField(verbose_name='留言时间', auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Blog留言',
                'verbose_name_plural': 'Blog留言',
            },
        ),
    ]
