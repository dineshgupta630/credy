# Generated by Django 2.0.13 on 2020-05-14 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200514_0031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='role',
            name='person',
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]