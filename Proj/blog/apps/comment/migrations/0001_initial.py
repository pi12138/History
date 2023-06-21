# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('email', models.CharField(verbose_name='邮箱', max_length=30, blank=True, null=True)),
                ('content', models.TextField(verbose_name='评论内容', blank=True, null=True)),
                ('pub_date', models.DateTimeField(verbose_name='评论时间', auto_now_add=True)),
                ('article', models.ForeignKey(verbose_name='文章ID', to='myblog.Article')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]
