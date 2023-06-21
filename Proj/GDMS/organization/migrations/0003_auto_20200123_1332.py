# Generated by Django 2.2 on 2020-01-23 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20200122_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='klass',
            name='faculty',
        ),
        migrations.AddField(
            model_name='klass',
            name='direction',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organization.Direction', verbose_name='所学方向'),
            preserve_default=False,
        ),
    ]
