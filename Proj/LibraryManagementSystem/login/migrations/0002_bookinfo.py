# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('ISBN', models.CharField(primary_key=True, max_length=12, serialize=False)),
                ('book_name', models.CharField(max_length=40)),
                ('book_author', models.CharField(max_length=20)),
                ('book_publish', models.CharField(max_length=20)),
                ('publication_date', models.DateTimeField()),
                ('book_num', models.IntegerField()),
            ],
            options={
                'db_table': 'book_info',
            },
        ),
    ]
