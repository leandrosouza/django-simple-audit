# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import copy

def ValuesQuerySetToDict(vqs):
    """converts a ValuesQuerySet to Dict"""
    return [item for item in vqs]


def get_m2m_fields_for(instance=None):
    """gets m2mfields for instance"""
    return instance._meta._many_to_many()


def get_m2m_values_for(instance=None):
    values = {}
    for m2m_field in get_m2m_fields_for(instance=instance):
        values[m2m_field.verbose_name] = ValuesQuerySetToDict(m2m_field._get_val_from_obj(instance).values())

    return copy.deepcopy(values)


def m2m_dict_diff(old, new):
    pass
