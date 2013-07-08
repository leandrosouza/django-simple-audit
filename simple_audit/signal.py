# -*- coding:utf-8 -*-
import logging
from django.db import models
from django.contrib.contenttypes.models import ContentType
from .models import Audit, AuditChange, AuditRequest
from .middleware import threadlocals

MODEL_LIST = set()
LOG = logging.getLogger(__name__)


def audit_m2m_change(sender, **kwargs):
    """
    TODO: audit m2m changes
    """
    if kwargs.get('action'):
        kwargs['m2m_change'] = True
        if kwargs['action'] == "pre_add":
            pass
        elif kwargs['action'] == "post_add":
            #save_audit(kwargs['instance'], Audit.CHANGE, kwargs=kwargs)
            pass
        elif kwargs['action'] == "pre_remove":
            pass
        elif kwargs['action'] == "post_remove":
            save_audit(kwargs['instance'], Audit.DELETE, kwargs=kwargs)
        elif kwargs['action'] == "pre_clear":
            pass
        elif kwargs['action'] == "post_clear":
            pass


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

            # signals for m2m fields
            m2ms = model._meta.get_m2m_with_model()
            if m2ms:
                for m2m in m2ms:
                    try:
                        sender_m2m = getattr(model, m2m[0].name).through
                        models.signals.m2m_changed.connect(audit_m2m_change, sender=sender_m2m)
                    except Exception, e:
                        LOG.warning("could not create signal for m2m field: %s" % e)


def register_m2m(*my_models):
    for model in my_models:
        if model is not None:
            models.signals.m2m_changed.connect(audit_m2m_change, sender=model)

NOT_ASSIGNED = object()


def get_or_create_audit_request(request_id):
    request = threadlocals.get_current_request()
    try:
        audit_request = AuditRequest.objects.get(request_id=request_id)
    except AuditRequest.DoesNotExist:
        audit_request = AuditRequest()
        audit_request.request_id = request_id
        audit_request.path = request.get_full_path()
        #get real ip
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            audit_request.ip = request.META['HTTP_X_FORWARDED_FOR']
        elif 'Client-IP' in request.META:
            audit_request.ip = request.META['Client-IP']
        else:
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
            class_name = value.__class__.__name__
            if hasattr(value, 'all'):
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


def save_audit(instance, operation, kwargs={}):
    """
    Saves the audit. 
    However, the variable persist_audit controls if the audit should be really
    saved to the database or not. This variable is only affected in a change operation. If no
    change is detected than it is setted to False.

    Keyword arguments:
    instance -- instance
    operation -- operation type (add, change, delete)
    kwargs -- kwargs dict sent from m2m signal
    """

    m2m_change = kwargs.get('m2m_change', False)

    try:
        persist_audit = True
        request_id = threadlocals.get_current_request_id()

        audit = Audit()
        audit.content_object = instance
        audit.operation = operation

        new_state = to_dict(instance)
        old_state = {}
        try:
            if operation == Audit.CHANGE and instance.pk:
                if not m2m_change:
                    old_state = to_dict(instance.__class__.objects.get(pk=instance.pk))
                else:
                    #TODO: m2m change
                    old_state = to_dict(instance.__class__.objects.get(pk=instance.pk))
        except:
            pass

        changed_fields = dict_diff(old_state, new_state)

        if operation == Audit.CHANGE:
            #is there any change?
            if not changed_fields:
                persist_audit = False
            audit.description = u'%s.' % (u"\n".join([u"%s: from %s to %s"
                % (k, format_value(v[0]), format_value(v[1])) for k, v in changed_fields.items()]))

        if request_id:
            audit.audit_request = get_or_create_audit_request(request_id)

        if persist_audit:
            audit.save()

            for field, (old_value, new_value) in changed_fields.items():
                change = AuditChange()
                change.audit = audit
                change.field = field
                change.new_value = new_value
                change.old_value = old_value
                change.save()
    except:
        LOG.error(u'Error registering auditing to %s: (%s) %s', repr(instance), type(instance),
                                                                getattr(instance, '__dict__', None))
