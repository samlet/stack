from typing import Text, Any, Dict, List, Union, Set
from sagas.nlu.inspector_common import Inspector, Context, cla_meta_intf
from sagas.nlu.utils import check_chain
from sagas.conf.conf import cf
import abc

def check_clause_sub(sents:Text, lang:Text, domain:Text, cla:Text,
          rel:Text, cats:Union[Text, Set, List]):
    """
    >>> from sagas.nlu.inspector_clauses import check_clause_sub
    >>> check_clause_sub(sents, 'pt', 'verb_domains', 'obl', 'cop', {'be'})
    :param sents:
    :param lang:
    :param domain:
    :param cla:
    :param rel:
    :param cats:
    :return:
    """
    from sagas.nlu.uni_chunks import get_chunk
    import sagas
    from sagas.nlu.ruleset_procs import list_words, cached_chunks, get_main_domains

    # cla = 'obl', rel = 'cop', cat='be'
    chunks = cached_chunks(sents, lang, cf.engine(lang))
    result = get_chunk(chunks, domain, cla,
                       lambda w: {'rel': w.dependency_relation,
                                  'pos': w.upos.lower(),
                                  'word': f"{w.text}/{w.lemma}"})

    word = next((w['word'] for w in result if w['rel'] == rel), None)
    if word:
        if isinstance(cats, str):
            return check_chain(cats, word, '*', lang)
        else:
            return any([check_chain(cat, word, '*', lang) for cat in cats])
    return False

class cla_expr(object):
    """
    >>> from sagas.nlu.inspector_common import cla_meta
    >>> from sagas.nlu.inspector_clauses import cla_expr
    >>> e=cla_expr('verb:obl', cop={'be'})
    >>> e.run('', cla_meta('Ela negou ser minha mãe.', 'pt'))
    """
    def __init__(self, domain_path:Text, **kwargs):
        self.domain_path=domain_path
        parts = domain_path.split(':')
        self.domain = f'{parts[0]}_domains'
        self.path = parts[1]
        self.chckers = kwargs

    def run(self, key, ctx:cla_meta_intf, operator=all):
        # check_clause_sub(sents, 'pt', 'verb_domains', 'obl', 'cop', {'be'})
        rs=[]
        for k,v in self.chckers.items():
            r=check_clause_sub(ctx.sents, ctx.lang, self.domain,
                             self.path, k, v)
            rs.append(r)
        return operator(rs)

    def __str__(self):
        return f"{self.domain_path}{self.chckers}"

    def __repr__(self):
        return self.__str__()

class ClausesInspector(Inspector):
    """
    >>> from sagas.nlu.inspector_clauses import ClausesInspector as clauses
    >>> clauses(all, cla_expr('verb:obl', cop={'be'})),
    """
    def __init__(self, operator, *exprs):
        self.operator=operator
        self.exprs=exprs

    def name(self):
        return "clauses"

    def run(self, key, ctx:Context):
        rs=[]
        for expr in self.exprs:
            r=expr.run(key, ctx)
            rs.append(r)
        return self.operator(rs)

    def __str__(self):
        return f"ins_{self.name()}({self.exprs})"

