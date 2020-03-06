# prototype: fn(results: List[Any], data:Dict[Text,Any])
sinkers_fn=[]
named_exprs={}

def registry_sinkers(*fn):
    sinkers_fn.extend(fn)

def registry_named_exprs(**kwargs):
    named_exprs.update(kwargs)
