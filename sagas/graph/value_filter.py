import datetime

from sagas.ofbiz.entities import OfEntity as e, oc
from sagas.ofbiz.entity_gen import get_dgraph_type
import json

def to_isoformat(datetime_val):
    dt=datetime.datetime.fromtimestamp(datetime_val/1000)
    return dt.isoformat()

def filter_json_val(model, json_val):
    result={}
    for k,v in json_val.items():
        if v is not None:
            if is_dt_field(model, k):
                result[k]=to_isoformat(v)
            else:
                result[k]=v
    return result

def is_dt_field(model, fld_name):
    fld=model.getField(fld_name)
    vt=get_dgraph_type(fld.getType())
    return vt=='datetime'

