# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_audit', '0002_auto_20150202_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='content_object_save',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
