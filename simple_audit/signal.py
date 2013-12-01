# -*- coding:utf-8 -*-
import logging
from django.db import models
from .models import Audit, AuditChange
from django.utils.translation import ugettext_lazy as _
import re


MODEL_LIST = set()
LOG = logging.getLogger(__name__)

def get_m2m_fields_for(instance=None):
    return instance._meta._many_to_many()

def get_m2m_values_for(instance=None):
    values = {}
    for m2m_field in get_m2m_fields_for(instance=instance):
        values[m2m_field] = (m2m_field._get_val_from_obj(instance).all())
    return values

def audit_m2m_change(sender, **kwargs):
    """
    TODO: audit m2m changes
    """
    if kwargs.get('action'):
        action = kwargs.get('action')
        instance = kwargs.get('instance')
        print "audit m2m_change > %s | %s" % (action, kwargs)
        print "*" * 30
        kwargs['m2m_change'] = True
        if kwargs['action'] == "pre_add":
            pass
        elif kwargs['action'] == "post_add":
            print "\t%s" % get_m2m_values_for(instance=instance)
            #save_audit(kwargs['instance'], Audit.CHANGE, kwargs=kwargs)
            # pass
        elif kwargs['action'] == "pre_remove":
            pass
        elif kwargs['action'] == "post_remove":
            save_audit(kwargs['instance'], Audit.DELETE, kwargs=kwargs)
        elif kwargs['action'] == "pre_clear":
            pass
        elif kwargs['action'] == "post_clear":
            pass


def audit_post_save(sender, **kwargs):
    print ">>> audit_post_save: %s" % kwargs
    print "*" * 30
    if kwargs['created']:
        save_audit(kwargs['instance'], Audit.ADD)


def audit_pre_save(sender, **kwargs):
    instance=kwargs.get('instance')
    print ">>> audit_pre_save: %s" % kwargs
    print "\t%s" % get_m2m_values_for(instance=instance)
    print "*" * 30
    if kwargs['instance'].pk:
        save_audit(kwargs['instance'], Audit.CHANGE)


def audit_pre_delete(sender, **kwargs):
    save_audit(kwargs['instance'], Audit.DELETE)


def register(*my_models):
    global MODEL_LIST
    for model in my_models:
        if model is not None:
            MODEL_LIST.add(model)
            models.signals.pre_save.connect(audit_pre_save, sender=model)
            models.signals.post_save.connect(audit_post_save, sender=model)
            models.signals.pre_delete.connect(audit_pre_delete, sender=model)

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


def get_value(obj, attr):
    """
    Returns the value of an attribute. First it tries to return the unicode value.
    """
    if hasattr(obj, attr):
        try:
            return getattr(obj, attr).__unicode__()
        except:
            value = getattr(obj, attr)
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
            if re.match(key, 'password'):
                old_value = 'xxxxxxxx'
                new_value = "*" * len(new.get(key))
            diff[key] = (old_value, new_value)

    return diff


def format_value(v):
    if isinstance(v, basestring):
        return u"'%s'" % v
    return unicode(v)


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
            description = u"\n".join([u"%s %s: %s %s %s %s" %
                (
                    _("field"),
                    k,
                    _("was changed from"),
                    format_value(v[0]),
                    _("to"),
                    format_value(v[1]),
                ) for k, v in changed_fields.items()])
        elif operation == Audit.DELETE:
            description = _('Deleted %s') % unicode(instance)
        elif operation == Audit.ADD:
            description = _('Added %s') % unicode(instance)

        LOG.debug("called audit with operation=%s instance=%s persist=%s" % (operation, instance, persist_audit))
        if persist_audit:
            audit = Audit.register(instance, description, operation)

            for field, (old_value, new_value) in changed_fields.items():
                change = AuditChange()
                change.audit = audit
                change.field = field
                change.new_value = new_value
                change.old_value = old_value
                change.save()
    except:
        LOG.error(u'Error registering auditing to %s: (%s) %s',
            repr(instance), type(instance), getattr(instance, '__dict__', None), exc_info=True)
