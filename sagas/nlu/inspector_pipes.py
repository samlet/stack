from typing import Text, Any, Dict, List, Union

from sagas.nlu.inspector_common import Context, Inspector

from blinker import NamedSignal, signal
import logging

from sagas.nlu.pipes import flat_table, pred_cond
from sagas.util.collection_util import wrap
# from sagas.nlu.pipes import *

logger = logging.getLogger(__name__)

class PipesInspector(Inspector):
    """
    Pipes inspector
    Instances: pipes(collect=['verb']),
        pipes(interr=pred_cond('/conj/cc', 'but')),
        pipes(pos=pred_cond('/conj', 'adj')),
        pipes(sense=sense_cond.is_cat('/obl', 'fact|事情')
                 .with_roles(domain='military|军')),
        pipes(cat=pred_cond('/conj', 'person')),

    Examples:
        $ shu 'A magas tanár nem angol, hanem magyar.'
    """
    def __init__(self, **kwargs):
        self.parameters=kwargs
        self.sigs_conf=[(signal(sig), paras) for sig,paras in kwargs.items()]

    def name(self):
        return "pipes"

    def get_domains(self, ctx:Context):
        from sagas.nlu.ruleset_procs import cached_chunks
        from sagas.conf.conf import cf

        # dn = lambda domain: f'{domain}_domains' if domain != 'predicts' else domain
        chunks = cached_chunks(ctx.sents, ctx.lang, cf.engine(ctx.lang))
        domains = chunks[ctx.domain_type]
        return domains

    def process_result(self, ctx:Context, results:List[Dict[Text, Any]]) -> bool:
        """
        Results sample:
        [{'name': 'collect_verb',
            'result': [token_data(word='think/think', pos='verb', path='/root')]}]
        :param results:
        :return:
        """
        has_result=False
        for result in results:
            logger.debug(result)
            vals=result['result']
            if vals:
                # 任意一个判定管道最终有输出, 即表示成功匹配,
                # 如果希望所有管道都必须有匹配才为真, 可以分成多个pipes(即多个inspector)编写,
                # 因为pattern的匹配规则就是所有inspectors均为真
                has_result=True
                path_val=ctx.domain_name+':'+vals[0]['path'][1:] if vals else '_'
                ctx.add_result(self.name(),
                               provider=f"{result['sig']}/{result['name']}",
                               part_name=path_val,
                               val=vals)
        return has_result

    def run(self, key, ctx:Context):
        # see also: procs-inspector-pipes.ipynb

        table_rs = []
        domains=self.get_domains(ctx)
        for ds in domains:
            flat_table(ds, '', table_rs)

        results = []
        for sig, paras in self.sigs_conf:
            if not bool(sig.receivers):
                logger.error(f"no receivers for {sig.name}")
            result = sig.send(self.name(), rs=table_rs, lang=ctx.lang, data=paras)
            if result:
                results.extend([{'name': fn.__name__, 'sig':sig.name, 'result': r} for fn, r in result])
        if results:  # 如果有连接函数, 就会有结果集, 但结果可能为空
            return self.process_result(ctx, results)
        else:
            return False

    def __str__(self):
        return f"ins_{self.name()}({self.parameters})"


class ExpressionInspector(Inspector):
    """
    Instances: ins().cat('/obj')=='animal',
    Examples:
        >>> rs =pat(ins().interr('/conj/cc')=='but',
        >>>         ins().pos('/conj')==['adj'],
        >>>         ins().cat('/conj')=='person',
        >>>         )
    """
    def __init__(self):
        self.callee = {}

    def name(self):
        return "exprs"

    def run(self, key, ctx: Context):
        pipes=PipesInspector

        if 'cond_val' in self.callee:
            # pipes(interr=pred_cond('/conj/cc', 'but')),
            ins=pipes(**{self.callee['sig']: pred_cond(
                self.callee['path'], self.callee['cond_val']
            )})
        elif 'cond_obj' in self.callee:
            # pipes(sense=sense_cond.is_cat('/obl', 'fact|事情')
            #                  .with_roles(domain='military|军')),
            ins =pipes(**{self.callee['sig']: self.callee['cond_obj']})
        else:
            # pipes(collect=['verb']),
            val=self.callee['value'] if 'value' in self.callee else None
            ins =pipes(**{self.callee['sig']: val})

        return ins.check(key, ctx)

    def __eq__(self, other):
        self.callee['cond_val']=other
        return self

    def __rshift__(self, other):
        self.callee['cond_obj']=other
        return self

    def __lt__(self, other):
        self.callee['value'] = other
        return self

    def __getattr__(self, method):
        def serv(path):
            self.callee={'sig': method, 'path': path}
            return self

        return serv

    def __str__(self):
        return f"ins_{self.name()}({', '.join(self.callee.keys())})"

