# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('user_account', models.CharField(max_length=12)),
                ('user_password', models.CharField(max_length=12)),
                ('user_age', models.IntegerField()),
                ('user_sex', models.CharField(max_length=10)),
                ('user_phone', models.CharField(max_length=12)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
    ]
