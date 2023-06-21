# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='博客标题', max_length=100)),
                ('category', models.CharField(verbose_name='博客标签', max_length=50)),
                ('pub_date', models.DateTimeField(verbose_name='发布时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', null=True, auto_now=True)),
                ('content', models.TextField(verbose_name='博客正文', blank=True, null=True)),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
            },
        ),
    ]
