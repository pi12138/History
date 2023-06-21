# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_bookinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('borrowing_time', models.DateTimeField()),
                ('return_time', models.DateTimeField(blank=True, null=True)),
                ('book_id', models.ForeignKey(to='login.BookInfo')),
                ('borrower_id', models.ForeignKey(to='login.UserInfo')),
            ],
            options={
                'db_table': 'borrow_info',
            },
        ),
    ]
