# -*- coding:utf-8 -*-

import logging

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

LOG = logging.getLogger(__name__)


class Audit(models.Model):
    ADD = 0
    CHANGE = 1
    DELETE = 2
    OPERATION_CHOICES = (
        (ADD, 'add'),
        (CHANGE, 'change'),
        (DELETE, 'delete')
    )
    operation = models.PositiveIntegerField(max_length=255, choices=OPERATION_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    audit_request = models.ForeignKey("AuditRequest", null=True)
    description = models.TextField()

    @property
    def operation_name(self):
        return dict(self.OPERATION_CHOICES)[self.operation]

    class Meta:
        db_table = 'audit'

    def __unicode__(self):
        return u"%s" % (self.operation)


class AuditChange(models.Model):
    audit = models.ForeignKey(Audit, related_name='field_changes')
    field = models.CharField(max_length=255)
    old_value = models.CharField(max_length=1024, null=True, blank=True)
    new_value = models.CharField(max_length=1024, null=True, blank=True)

    class Meta:
        db_table = 'audit_change'


class AuditRequest(models.Model):
    request_id = models.CharField(max_length=255)
    ip = models.IPAddressField()
    path = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'audit_request'
