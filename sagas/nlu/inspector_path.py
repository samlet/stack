from sagas.nlu.inspector_common import Inspector, Context
from sagas.conf.conf import cf
import sagas.tracker_fn as tc
import logging
logger = logging.getLogger(__name__)

def normal_path(path):
    prefix='$.'
    suffix='.text,lemma'
    parts=path.split('/')
    parts_str='.'.join([f"{t}[*]" for t in parts])
    return f"{prefix}{parts_str}{suffix}"

class PathInspector(Inspector):
    def __init__(self, path, kind, pos='*', domains='verb', engine=None, match_method='any'):
        self.paths=path if isinstance(path, list) else [path]
        self.kind=kind
        self.pos=pos
        self.match_method=match_method
        self.engine=engine
        self.domains=domains

    def name(self):
        return "ins_path"

    def run(self, key, ctx:Context):
        from jsonpath_ng import jsonpath, parse
        from sagas.nlu.inspector_wordnet import predicate
        from sagas.nlu.ruleset_procs import cached_chunks

        lang=ctx.lang
        domain_name=f"{self.domains}_domains"  # like: 'verb_domains'
        parsers = [parse(normal_path(expr)) for expr in self.paths]
        results=[]
        engine=cf.engine(lang) if self.engine is None else self.engine
        chunks = cached_chunks(ctx.sents, lang, engine)
        for chunk in chunks[domain_name]:
            json_data = chunk
            # for expr in exprs:
            for parser in parsers:
                # print([(match.value, str(match.full_path)) for match in parser.find(json_data)])
                word = '/'.join([match.value for match in parser.find(json_data)])
                pred_r=predicate(self.kind, word, lang, self.pos)
                tc.emp('yellow' if not pred_r else 'green', f".. {word} is {self.kind}: {pred_r}")
                results.append(pred_r)

        logger.debug(f"{results}")
        return any(results) if self.match_method=='any' else all(results)

    def __str__(self):
        return "{}({} {} is {}@{})".format(self.name(), self.match_method, ', '.join(self.paths), self.kind, self.pos)

pred_any_path=lambda path, kind, pos='*', engine=None: PathInspector(path, kind, pos, domains='verb', match_method='any')
pred_all_path=lambda path, kind, pos='*', engine=None: PathInspector(path, kind, pos, domains='verb', match_method='all')
any_path=lambda path, kind, pos='*', engine=None: PathInspector(path, kind, pos, domains='root', match_method='any')

