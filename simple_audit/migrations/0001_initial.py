# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('operation', models.PositiveIntegerField(max_length=255, verbose_name='Operation', choices=[(0, 'add'), (1, 'change'), (2, 'delete')])),
                ('object_id', models.PositiveIntegerField(db_index=True)),
                ('description', models.TextField()),
                ('obj_description', models.CharField(db_index=True, max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'audit',
                'verbose_name': 'Audit',
                'verbose_name_plural': 'Audits',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuditChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=255)),
                ('old_value', models.TextField(null=True, blank=True)),
                ('new_value', models.TextField(null=True, blank=True)),
                ('audit', models.ForeignKey(related_name='field_changes', to='simple_audit.Audit')),
            ],
            options={
                'db_table': 'audit_change',
                'verbose_name': 'Audit',
                'verbose_name_plural': 'Audits',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AuditRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('request_id', models.CharField(max_length=255)),
                ('ip', models.IPAddressField()),
                ('path', models.CharField(max_length=1024)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'audit_request',
                'verbose_name': 'Audit',
                'verbose_name_plural': 'Audits',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='audit',
            name='audit_request',
            field=models.ForeignKey(to='simple_audit.AuditRequest', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='audit',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
            preserve_default=True,
        ),
    ]
