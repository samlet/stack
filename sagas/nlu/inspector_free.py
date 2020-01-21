from typing import Text, Any, Dict, List
from sagas.nlu.inspector_common import Inspector, Context
from sagas.nlu.ruleset_procs import cached_chunks
from sagas.conf.conf import cf
import logging

logger = logging.getLogger(__name__)

def is_noun_desc(ctx:Context, domain):
    sents, lang=ctx.sents, ctx.lang
    chunks = cached_chunks(sents, lang, cf.engine(lang))
    domains = chunks[domain]
    domain = domains[0]
    comps = [k for k, v in domain.items() if isinstance(v, list)]
    logger.debug(f'.. {comps}')
    return domain['upos']=='NOUN' and \
            all(c for c in comps if c.endswith('mod') or c in ('punct'))

checker_mappings={
    'noun_desc':is_noun_desc,
}
class CompsInspector(Inspector):
    """
    # $ sid 'Tidak banyak pohon di gurun.'
    >>> pat(5, name='noun_desc').root(comps(noun_desc=True)),
    """
    def __init__(self, domain, **kwargs):
        self.domain=domain if domain.endswith('_domains') else domain+'_domains'
        self.checkers=kwargs

    def name(self):
        return "comps"

    def run(self, key:Text, ctx:Context):
        result=[]
        for k,v in self.checkers.items():
            logger.debug(f".. check {k}=={v}")
            r=checker_mappings[k](ctx, self.domain)
            result.append(r)
        return all(result)

    def __str__(self):
        return f"{self.name()}({self.checkers})"

comps=lambda **kwargs: CompsInspector('root', **kwargs)

class PredictsInspector(Inspector):
    """
    # $ se 'what will be the weather in three days?'
    >>> pat(5, name='query_weather').root(predict_aux(
                ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')])),
    """
    def __init__(self, domain, checker):
        self.domain=domain if domain.endswith('_domains') else domain+'_domains'
        self.checker=checker

    def name(self):
        return "predicts"

    def run(self, key:Text, ctx:Context) -> bool:
        from sagas.nlu.predicts import predicate
        from sagas.nlu.operators import ud

        final_rs = []

        sents, lang = ctx.sents, ctx.lang
        chunks = cached_chunks(sents, lang, cf.engine(lang))
        domains = chunks[self.domain]
        for el in domains:
            # logger.debug(f"`{el['lemma']}` >> *{el['dc']['lemma']}*")
            # r1 = predicate(el, ud.__text('will') >> [ud.nsubj('what'), ud.dc_cat('weather')], lang)
            r1 = predicate(el, self.checker, lang)
            # r2=predicate(el, ud.__cat('be') >> [ud.nsubj('what'), ud.dc_cat('animal/object')], lang)
            result = all([r[0] for r in r1])
            final_rs.append(result)
            logger.debug(f"{r[0] for r in r1}, {result}")
        return any(final_rs)

    def __str__(self):
        return f"{self.name()}"

predict_aux=lambda c: PredictsInspector('aux', c)
predict_subj=lambda c: PredictsInspector('subj', c)
predict_verb=lambda c: PredictsInspector('verb', c)

