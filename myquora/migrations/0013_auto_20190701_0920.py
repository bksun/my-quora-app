# Generated by Django 2.2.2 on 2019-07-01 09:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myquora', '0012_auto_20190701_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2019, 7, 1, 9, 20, 53, 73698), null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='date_updated',
            field=models.DateField(default=datetime.datetime(2019, 7, 1, 9, 20, 53, 73724), null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2019, 7, 1, 9, 20, 53, 72384), null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2019, 7, 1, 9, 20, 53, 74465), null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='date_updated',
            field=models.DateField(default=datetime.datetime(2019, 7, 1, 9, 20, 53, 74486), null=True),
        ),
        migrations.AlterField(
            model_name='upvote',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2019, 7, 1, 9, 20, 53, 71785)),
        ),
    ]