# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedBackInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('user_account', models.CharField(max_length=12)),
                ('opinion_content', models.TextField()),
                ('issuing_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'feedback_info',
            },
        ),
    ]
