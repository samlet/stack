from typing import Text, Any, Dict, List, Union, Optional
from sagas.util.string_util import base64, unbase64
from six import text_type

def to_global_id(type:Text, id:Text):
    '''
    Takes a type name and an ID specific to that type name, and returns a
    "global ID" that is unique among all types.
    '''
    return base64(':'.join([type, text_type(id)]))


def from_global_id(global_id:Text):
    '''
    Takes the "global ID" created by toGlobalID, and retuns the type name and ID
    used to create it.
    '''
    unbased_global_id = unbase64(global_id)
    _type, _id = unbased_global_id.split(':', 1)
    return _type, _id
