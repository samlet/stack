from sagas.nlu.patterns import Patterns

def verb(*args, **kwargs):
    return {'method':'verb', 'args':args, 'kwargs':kwargs}
def subj(*args, **kwargs):
    return {'method':'subj', 'args':args, 'kwargs':kwargs}

def chained(pat:Patterns, *args):
    coll=[]
    for insp in args:
        serv=pat.prepare(insp['method'])
        r=serv(*insp['args'], **insp['kwargs'])
        coll.append(r)
        # if the pattern failed to match, stop execute the succeed patterns
        if not r[1]:
            return []
    return coll


