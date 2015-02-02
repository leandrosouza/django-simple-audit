# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simple_audit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit',
            name='object_id',
            field=models.TextField(db_index=True),
            preserve_default=True,
        ),
    ]
