# Generated by Django 3.1.7 on 2021-03-15 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20210315_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposition',
            name='work_experience',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='工作经验'),
        ),
    ]
