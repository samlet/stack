# prototype: fn(results: List[Any], data:Dict[Text,Any])
sinkers_fn=[]

def registry_sinkers(*fn):
    sinkers_fn.extend(fn)
