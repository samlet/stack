import logging
logger = logging.getLogger(__name__)

def eval_path(domains, path):
    from jsonpath_ng import jsonpath, parse

    if path.startswith('__'):
        return domains['lemma']+'/'+domains['text']
    else:
        prefix='$.'
        suffix='.text,lemma'
        parts=path.split('/')
        parts_str='.'.join([f"{t}[*]" for t in parts])
        expr= f"{prefix}{parts_str}{suffix}"
        parser=parse(expr)
        word = '/'.join([match.value for match in parser.find(domains)])
        return word

def desc_expr(el, domains, lang):
    from sagas.nlu.inspector_wordnet import predicate

    if el._type.startswith('__'):
        comp='__'
        sub = el._type
        oper=el._type[2:]
    elif el._type.startswith('_'):  # is a function in a class
        # like: _PredictSamples__text
        comp='__'
        oper=el._type.split('__')[1]
        sub='__'+oper
    elif '_' in el._type:
        parts=el._type.split('_')
        comp=f"{parts[0]}'s {parts[1]}"
        sub=parts[0]
        oper=parts[1]
    else:
        comp=f"{el._type}'s lemma"
        sub=el._type
        oper='equals'
    val=', '.join(el._right)
    cond=eval_path(domains, sub)
    eq=lambda vals: any([v in vals for v in cond.split('/')])
    oper_mappings={'equals': eq,
                   'text': eq,
                   'cat': lambda vals: any([predicate(e, cond, lang, '*') for e in vals])
                   }
    if oper in oper_mappings:
        result=oper_mappings[oper](el._right)
        msg=''
    else:
        result=False
        msg=f'invalid operator {oper}'
    logger.debug(f"- `{comp}` {el._op} `{val}`, *{cond}* -> {result} {msg}")

    return result, msg

def predicate(domains, val, lang):
    results=[]
    logger.debug(f"*{val._left._type}* {val._left._op} {val._left._right}")
    results.append(desc_expr(val._left, domains, lang))

    # desc_expr(val._left)
    expr=val._right
    if isinstance(expr, list):
        for el in expr:
            results.append(desc_expr(el, domains, lang))
    else:
        results.append(desc_expr(expr, domains, lang))
    return results

