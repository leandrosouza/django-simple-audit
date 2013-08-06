# -*- coding:utf-8 -*-

import logging
import threading
import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _


LOG = logging.getLogger(__name__)


class Audit(models.Model):
    ADD = 0
    CHANGE = 1
    DELETE = 2
    OPERATION_CHOICES = (
        (ADD, _('add')),
        (CHANGE, _('change')),
        (DELETE, _('delete'))
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    operation = models.PositiveIntegerField(max_length=255, choices=OPERATION_CHOICES, verbose_name=_('Operation'))
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

    THREAD_LOCAL = threading.local()

    request_id = models.CharField(max_length=255)
    ip = models.IPAddressField()
    path = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Date"))
    user = models.ForeignKey(User)

    class Meta:
        db_table = 'audit_request'

    @staticmethod
    def new_request(path, user, ip):
        """
        Create a new request from a path, user and ip and put it on thread context.
        The new request not be saved until first use or calling method current_request(True)
        """
        audit_request = AuditRequest()
        audit_request.ip = ip
        audit_request.user = user
        audit_request.path = path
        audit_request.request_id = uuid.uuid4().hex
        AuditRequest.THREAD_LOCAL.current = audit_request
        return audit_request

    @staticmethod
    def set_request_from_id(request_id):
        """ Load an old request from database and put it again in thread context. If request_id doesn't
        exist, thread context will be cleared """
        try:
            audit_request = AuditRequest.objects.get(request_id)
            AuditRequest.THREAD_LOCAL.current = audit_request
            return audit_request
        except AuditRequest.DoesNotExist:
            AuditRequest.THREAD_LOCAL.current = None
            return None

    @staticmethod
    def current_request(force_save=False):
        """ Get current request from thread context (or None doesn't exist). If you specify force_save,
        current request will be saved on database first.
        """
        audit_request = getattr(AuditRequest.THREAD_LOCAL, 'current', None)
        if force_save and audit_request is not None and audit_request.pk is None:
            audit_request.save()
        return audit_request

    @staticmethod
    def cleanup_request():
        """
        Remove audit request from thread context
        """
        AuditRequest.THREAD_LOCAL.current = None

