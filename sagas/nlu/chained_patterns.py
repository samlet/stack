from sagas.nlu.patterns import Patterns

def verb(*args, **kwargs):
    return {'method':'verb', 'args':args, 'kwargs':kwargs}
def subj(*args, **kwargs):
    return {'method':'subj', 'args':args, 'kwargs':kwargs}

def chained(pat:Patterns, *args):
    """
    Examples:
        # $ sj 父は私にとてもきびしかった。
        # $ sj 本田先生は学生たちにきびしそうだ。
        chained(pat(5, name='desc_attitude'),
                subj('adj', ガ=agency),
                verb(extract_for('plain', 'ガ'),
                     extract_for('plain', 'ニ'),
                     extract_for('plain', '修飾'),
                     specsof('*', 'tight'),
                     )
                ),
    :param pat:
    :param args:
    :return:
    """
    coll=[]
    for insp in args:
        serv=pat.prepare(insp['method'])
        r=serv(*insp['args'], **insp['kwargs'])
        coll.append(r)
        # if the pattern failed to match, stop execute the succeed patterns
        if not r[1]:
            return []
    return coll


