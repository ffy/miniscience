# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 08:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='author',
        ),
        migrations.AddField(
            model_name='publication',
            name='author',
            field=models.ManyToManyField(to='publications.Author'),
        ),
    ]