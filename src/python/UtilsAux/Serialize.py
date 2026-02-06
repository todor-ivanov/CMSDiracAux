#! /usr/bin/env python

import json
import pickle,sys,pprint
import inspect
from collections.abc import Iterable


def serializeObj_(obj):
    """
    _serializeObj_
    Returns a serialized dictionary
    """
    if _isSerializable(obj):
        return obj

    if not isinstance(obj, Iterable):
        if _isSerializable(obj):
            return obj
        else:
            return str(obj)

    # Check if the object is still iterable but one of str or bytes
    # Avoid TypeError: Object of type bytes is not JSON serializable
    if isinstance(obj, str) or isinstance(obj, bytes):
        return str(obj)

    # Check if the object has any of the WMCore.Configuration dictionary representation methods:
    for membName, memb in inspect.getmembers(obj):
        outputD = dict()
        if inspect.ismethod(memb) and membName == 'dictionary_whole_tree_':
            for key, value in serializeObj_(obj.dictionary_whole_tree_()).items():
                outputD[key] = serializeObj_(value)
            return outputD
        elif inspect.ismethod(memb) and membName == 'dictionary_':
            for key, value in serializeObj_(obj.dictionary_()).items():
                outputD[key] = serializeObj_(value)
            return outputD
        else:
            continue

    if isinstance(obj, (list, set, tuple)):
        outputList = list()
        if _isSerializable(obj):
            return obj
        else:
            for value in obj:
                outputList.append(serializeObj_(value))
            return outputList

    elif isinstance(obj, dict):
        outputD = dict()
        if _isSerializable(obj):
            return obj
        else:
            for key, value in obj.items():
                outputD[key] = serializeObj_(value)
            return outputD

    else:
        print(f"ERROR: Unrecognized iterable obj: {obj} of type {type(obj)}")
        raise TypeError

def _isSerializable(obj):
    """
    __isSerializable__
    Auxiliary function to check for object serialization
    :param obj: Object of any type to be checked
    :return:    Bool - True if the object is serializable, False otherwise
    """
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False
