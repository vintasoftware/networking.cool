# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0002_auto_20151115_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='attendee',
            field=models.ForeignKey(related_name='concepts', to='attendees.Attendee'),
        ),
    ]
