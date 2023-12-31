# Generated by Django 2.2.3 on 2022-03-19 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('nickname', models.CharField(max_length=30, verbose_name='昵称')),
                ('github', models.URLField(verbose_name='github地址')),
                ('email', models.EmailField(max_length=200, verbose_name='邮箱')),
                ('location', models.CharField(max_length=30, verbose_name='地理位置')),
                ('avatar', models.FileField(max_length=200, upload_to='media/userinfo_image/', verbose_name='头像')),
                ('words', models.TextField(verbose_name='想说啥')),
                ('used', models.IntegerField(choices=[(1, 'YES'), (0, 'NO')], default=0, verbose_name='使用')),
            ],
            options={
                'verbose_name': '个人信息',
                'verbose_name_plural': '个人信息',
            },
        ),
    ]
