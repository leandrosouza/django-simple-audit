# -*- coding:utf-8 -*-
import logging
from django.db import models
from django.contrib.contenttypes.models import ContentType
from .models import Audit, AuditChange, AuditRequest
from .middleware import threadlocals

MODEL_LIST = set()
LOG = logging.getLogger(__name__)


def audit_post_save(sender, **kwargs):
    if kwargs['created']:
        save_audit(kwargs['instance'], Audit.ADD)


def audit_pre_save(sender, **kwargs):
    if kwargs['instance'].pk:
        save_audit(kwargs['instance'], Audit.CHANGE)


def audit_post_delete(sender, **kwargs):
    save_audit(kwargs['instance'], Audit.DELETE)


def register(*my_models):
    global MODEL_LIST
    for model in my_models:
        if model is not None:
            MODEL_LIST.add(model)
            models.signals.pre_save.connect(audit_pre_save, sender=model)
            models.signals.post_save.connect(audit_post_save, sender=model)
            models.signals.post_delete.connect(audit_post_delete, sender=model)

NOT_ASSIGNED = object()


def get_or_create_audit_request(request_id):
    request = threadlocals.get_current_request()
    try:
        audit_request = AuditRequest.objects.get(request_id=request_id)
    except AuditRequest.DoesNotExist:
        audit_request = AuditRequest()
        audit_request.request_id = request_id
        audit_request.path = request.get_full_path()
        audit_request.ip = request.META['REMOTE_ADDR']
        audit_request.user = threadlocals.get_current_user()
        audit_request.save()
    return audit_request

def get_value(obj, attr):
    """
    Returns the value of an attribute. First it tries to return the unicode value.
    """
    if hasattr(obj, attr):
        try:
            return getattr(obj, attr).__unicode__()
        except:
            value = getattr(obj, attr)
            if value.__class__.__name__ == 'RelatedManager':
                return [v.__unicode__() for v in value.all()]
            else:
                return value
    else:
        return None

def to_dict(obj):
    if obj is None:
        return {}

    if isinstance(obj, dict):
        return dict.copy()

    state = {}            

    for key in obj._meta.get_all_field_names():
        state[key] = get_value(obj, key)

    return state

def dict_diff(old, new):

    keys = set(old.keys() + new.keys())
    diff = {}
    for key in keys:
        old_value = old.get(key, None)
        new_value = new.get(key, None)
        if old_value != new_value:
            diff[key] = (old_value, new_value)
            
    return diff


def format_value(v):
    return str(v)


def save_audit(instance, operation):

    try:
        save_audit = True
        request_id = threadlocals.get_current_request_id()

        audit = Audit()
        audit.content_object = instance
        audit.operation = operation

        new_state = to_dict(instance)
        old_state = {}
        try:
            if operation == Audit.CHANGE and instance.pk:
                old_state = to_dict(instance.__class__.objects.get(pk=instance.pk))
        except:
            pass

        changed_fields = dict_diff(old_state, new_state)
            
        if operation == Audit.CHANGE:
            #is there any change?
            if not changed_fields:
                save_audit = False
            audit.description = u'%s.' % (u"\n".join([u"%s: from %s to %s"
                % (k, format_value(v[0]), format_value(v[1])) for k, v in changed_fields.items()]))

        if request_id:
            audit.audit_request = get_or_create_audit_request(request_id)

        if save_audit:
            audit.save()
        
            for field, (old_value, new_value) in changed_fields.items():
                change = AuditChange()
                change.audit = audit
                change.field = field
                change.new_value = new_value
                change.old_value = old_value
                change.save()
    except:
        LOG.error(u'Error registering auditing to %s: (%s) %s', repr(instance), type(instance), getattr(instance, '__dict__', None))
