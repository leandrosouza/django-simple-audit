# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import copy
from pprint import pprint

LOG = logging.getLogger(__name__)

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

def normalize_dict(d):
    """removes datetime objects and passwords"""
    for k in d.keys():
        if d.get(k).find('password') != -1:
            d[k] = 'xxxxx'
            
    return d
    
def m2m_clean_unchanged_fields(dict_diff):
    """
    returns a list of dicts with only the changes
    """
    dict_list = []
    for key in dict_diff.keys():
        new_dict = {}
        dict_ = dict_diff.get(key)
        
        for value in dict_.keys():
            compound_key = "%s.%s" % (key, value)
            if dict_[value][0] == dict_[value][1]:
                del dict_[value]
            else:
                new_dict[compound_key] = dict_[value]
        
        del dict_diff[key]
        if new_dict:
            dict_list.append(new_dict)

    return dict_list

def m2m_dict_diff(old, new):
    # print("m2m old: %s" % (old))
    # print("m2m new: %s" % (new))

    diff = {}
    field_name = None
    
    #old is empty?
    swap = False
    if not old:
        #set old to new, then swap elements at the end
        old = new
        new = {}
        swap = True
    
    #first create empty diff based in old state
    for key in old.keys():
        if not field_name:
            field_name = key
        else:
            if field_name != key:
                LOG.warning("ops... field_name name change detected")
        #oldstate
        id_=0
        for item in old[key]:
            empty_dict={}
            for key_ in item.keys():
                # print "key: %s" % key_
                if key_ == "id":
                    id_=item[key_]
                empty_dict[key_] = [item[key_], None]

            diff["%s.%s" % (field_name, id_)] = empty_dict

        #new state
        #discover id
        empty_dict={}
        id=0

        for item in new.get(key, []):
            for key_ in item.keys():
                if key_ == "id":
                    id=item[key_]
                    break
            break

        #check if the id exists in old state
        key_name = "%s.%s" % (field_name, id)
        id_exists = key_name in diff

        for item in new.get(key, []):
            for key_ in item.keys():
                if id_exists:
                    diff[key_name][key_][1] = item[key_]
                else:
                    empty_dict[key_] = [None, item[key_]]


            if not id_exists:
                diff["%s.%s" % (field_name, id)] = empty_dict

    #clean unchanged fields
    diff = m2m_clean_unchanged_fields(diff)
    if swap:
        for dif in diff:
            for key in dif.keys():
                el_0 = dif[key][1]
                el_1 = dif[key][0]
                dif[key][0] = el_0
                dif[key][1] = el_1
    if diff:
        LOG.debug("m2m diff cleaned: %s" % pprint(diff))
    return diff

def persist_m2m_audit():
    pass