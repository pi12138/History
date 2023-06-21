# Generated by Django 2.2 on 2020-01-22 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='profession',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organization.Profession', verbose_name='所属专业'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='klass',
            name='faculty',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organization.Faculty', verbose_name='所属学院'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='office',
            name='faculty',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organization.Faculty', verbose_name='所属学院'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profession',
            name='faculty',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='organization.Faculty', verbose_name='所属学院'),
            preserve_default=False,
        ),
    ]