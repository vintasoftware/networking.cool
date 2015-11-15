# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendee',
            name='company',
            field=models.CharField(max_length=255, blank=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='picture',
            field=models.TextField(blank=True),
        ),
    ]
