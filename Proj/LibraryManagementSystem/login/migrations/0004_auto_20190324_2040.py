# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_borrowinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='user_password',
            field=models.CharField(max_length=40),
        ),
    ]
