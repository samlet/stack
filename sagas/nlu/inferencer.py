from typing import Text, Any, Dict, List, Union, Tuple
import requests
from sagas.conf.conf import cf
from sagas.nlu.inspector_common import Context
from sagas.nlu.patterns import Patterns
from sagas.nlu.rules_meta import build_meta
import sagas.tracker_fn as tc
from sagas.nlu.utils import join_text
import sagas
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

# def fix_data(data):
#     if 'engine' not in data:
#         data['engine'] = cf.engine(data['lang'])
#     data['sents']=fix_sents(data['sents'], data['lang'])
#     return data

def parse(data):
    if 'engine' not in data:
        data['engine']=cf.engine(data['lang'])
    engine=data['engine']
    response = requests.post(f'{cf.servant(engine)}/verb_domains', json=data)
    if response.status_code == 200:
        return response.json()
    return None

def norm_arg(arg):
    return arg.replace(':', '_')

class InferExtensionPoints(object):
    def __init__(self):
        self.exts={}
        self.exists=lambda key: key in self.exts

    @property
    def extensions(self) -> Dict[Text, List[Any]]:
        return self.exts
    def register(self, key, val):
        if key in self.exts:
            self.exts[key].append(val)
        else:
            self.exts[key]=[val]
    def value(self, key):
        if key in self.exts:
            return self.exts[key][0]
        return None
    def values(self, key):
        return self.exts[key]

    def register_parts(self, lang, fn_map):
        for k,f in fn_map.items():
            ext_point = f"part.{lang}.{k}"
            self.register(ext_point, f)

    def register_domains(self, lang, fn_map):
        for k,f in fn_map.items():
            ext_point = f"domain.{lang}.{k}"
            self.register(ext_point, f)

extensions=InferExtensionPoints()

class DomainToken(object):
    def __init__(self, **kwargs):
        self.props=kwargs

    @property
    def type_name(self):
        return self.props['type']

    @property
    def type(self):
        return self.props['type']

    @property
    def lang(self):
        return self.props['lang']
    @property
    def text(self):
        return self.props['text']

    @property
    def lemma(self):
        return self.props['lemma']
    @property
    def index(self):
        return self.props['index']

    @property
    def head(self):
        return self.props['head']

    @property
    def head_trans(self):
        return self.props['head_trans']

    @property
    def translit(self):
        return self.props['translit']

    @property
    def translate(self):
        return self.props['translate']

    @property
    def rels(self) -> List[Text]:
        return self.props['rels']

    @property
    def ctx(self) -> Context:
        return self.props['ctx']

    @property
    def stems(self) -> List[Tuple[Text,Text]]:
        return self.props['stems']

    def pattern(self, dominator='verb', priority=5, name='_noname_'):
        """
        >>> from sagas.nlu.rules_header import *
        >>> pat=token.pattern('verb')
        >>> r=pat(behaveof('eat', 'v'))
        >>> assert r[1]
        >>> r=pat(obl=kindof('building', 'n'))
        >>> assert r[1]
        :param dominator:
        :param priority:
        :param name:
        :return:
        """
        ctx=self.ctx
        domain=dominator.split('_')[0]
        pat = Patterns(ctx.domains, ctx.meta, priority=priority, name=name)
        serv = pat.prepare(domain)
        return serv

@dataclass_json(letter_case=LetterCase.CAMEL)  # all fields are encoded/decoded from camelCase
@dataclass
class InferPart:
    name: str
    chunk: str
    text: str
    lemma: str
    translit: str
    translate: str
    index: int
    domain: DomainToken=None

    @property
    def word(self) -> str:
        return f"{self.text}/{self.lemma}"

class Inferencer(object):
    def __init__(self, lang):
        self.lang=lang

    def proc_word(self, type_name:Text, word:Text, head:Text, index:int, r, lang:Text) -> Dict[Text, Any]:
        from sagas.tool.misc import translit_chunk, display_synsets, target_lang
        from sagas.nlu.google_translator import translate
        res, _ = translate(word, source=lang, target=target_lang(lang),
                           trans_verbose=False)

        # result=f"[{type_name}]({word}{translit_chunk(word, lang)}) {res}{target}"
        result = {'type': type_name,
                  'text': word,
                  'lemma': r['lemma'],
                  'translit': translit_chunk(word, lang),
                  'translate': res,
                  'lang': lang,
                  'index': index,
                  }
        if head != '':
            res_t, _ = translate(head, source=lang, target=target_lang(lang),
                                 trans_verbose=False, options={'disable_correct'})
            # target=f" ⊙︿⊙ {res_t}({head})"
            result['head'] = head
            result['head_trans'] = res_t
        # tc.emp('magenta', result)
        return result

    # def proc_children_column(partcol, textcol, idxcol, lang):
    def proc_children_column(self, df, lang:Text) -> List[InferPart]:
        from sagas.nlu.google_translator import translate
        from sagas.tool.misc import translit_chunk, display_synsets, target_lang
        result = []
        # for id, (name, r) in enumerate(zip(partcol, textcol)):
        rels = []
        for id, row in df.iterrows():
            # df['rel'], df['children'], df['index']
            name, r, idx = row['rel'], row['children'], row['index']
            if name in rels:
                continue
            else:
                rels.append(name)
            if name not in ('punct', 'head_root'):
                sent = join_text(r, lang)
                res, _ = translate(sent, source=lang, target=target_lang(lang),
                                   trans_verbose=False, options={'disable_correct'})
                # chunk=f"{indent}[{name}]({sent}{translit_chunk(sent, lang)}) {res}"
                chunk = InferPart(name= name,
                         chunk= sent,
                         text= row['text'],
                         lemma= row['lemma'],
                         translit= translit_chunk(sent, lang),
                         translate= res,
                         index= idx,
                )
                result.append(chunk)
                # tc.emp('cyan', chunk)
        return result

    def induce_spec(self, el, pats:List[Tuple[int, Text]], type_name:Text) -> None:
        # print(f"{el.indicator} {el.word}: {el.spec}")
        if el.indicator == '[verb]':
            pats.append((3, f"behaveof('{el.spec}', 'v')"))
        elif el.indicator == '[aux]':
            # pats.append((3, f"behaveof('{el.spec}', '*')"))
            pass
        elif el.indicator == '[root]':
            pats.append((3, f"behaveof('{el.spec}', 'n')"))
        elif el.indicator == '[predicate]':
            pats.append((3, f"specsof('*', '{el.spec}')"))
        else:
            if type_name in ('aux_domains', 'subj_domains') and el.indicator == 'head':
                pats.append((3, f"behaveof('{el.spec}', '*')"))
            else:
                pats.append((1, f"{norm_arg(el.indicator)}=kindof('{el.spec}', '*')"))

    def induce_part(self, chunk:InferPart, pats:List[Tuple[int, Text]],
                    type_name:Text, enable_verbose=False):
        if enable_verbose:
            tc.emp('cyan', chunk)


        ext_point=f"part.{self.lang}.{chunk.name}"
        global_point=f"part.*.{chunk.name}"
        fn=extensions.value(ext_point) or extensions.value(global_point)
        logger.debug(f".. get extension from {ext_point}: {fn}")
        fnr=None
        if fn:
            fnr=fn(chunk, type_name)
        # if fnr is None and chunk.name in gen_map:
        #     fnr=gen_map[chunk.name]()

        if fnr:
            if isinstance(fnr, list):
                pats.extend(fnr)
            else:
                pats.append(fnr)

    def induce_domain_from_exts(self, chunk:DomainToken,
                                domain: Text, pats:List[Text]):
        ext_point = f"domain.{self.lang}.{domain}"
        fn = extensions.value(ext_point)
        logger.debug(f".. get extension from {ext_point}: {fn}")
        if fn:
            fnr = fn(chunk, domain)
            if fnr:
                if isinstance(fnr, list):
                    pats.extend(fnr)
                else:
                    pats.append(fnr)

    def induce_pattern(self, pat:DomainToken, ds, enable_verbose=False) -> Text:
        if enable_verbose:
            tc.emp('magenta', pat)

        def gen_verb(ind='verb', prefix='behave'):
            spec = [d for d in ds if d['indicator'] == f'[{ind}]']
            if spec:
                ref = spec[0]['spec']
            else:
                ref = pat.translate.replace(' ', '_')
            return f"pat(5, name='{prefix}_{ref}').verb"

        def gen_root():
            spec = [d for d in ds if d['indicator'] == '[root]']
            if spec:
                ref = spec[0]['spec']
            else:
                ref = pat.translate.replace(' ', '_')
            return f"pat(5, name='ana_{ref}').root"

        def gen_cop():
            spec = [d for d in ds if d['indicator'] == 'head']
            if spec:
                ref = spec[0]['spec']
            else:
                ref = pat.head_trans.replace(' ', '_') if pat.lang != 'en' else pat.head.replace(' ', '_')
            return f"pat(5, name='desc_{ref}').cop"

        domap = {'verb_domains': gen_verb,
                 'aux_domains': gen_cop,
                 'subj_domains': gen_cop,
                 'root_domains': gen_root,
                 'predicate': lambda: gen_verb('predicate', 'predict'),
                 }
        return domap[pat.type]().lower()

    def stem_chunks(self, r):
        tuple_list=[] # 使用tuple-list是因为一个句子会有重复的成分
        for stem in r['stems']:
            # if stem[0] in stem_filters:
            # stem[1]是一个列表, 包含了所有的word-lemmas
            if stem[1]:
                value = ' '.join(stem[1])
                # stem[0]是成分名称, 比如obj/obl/nsubj/...
                tuple_list.append((stem[0], value))
        return tuple_list

    def infer(self, sents, verbose=False) -> List[Text]:
        from sagas.tool.misc import translit_chunk, display_synsets, target_lang
        data = {'lang': self.lang, "sents": sents}
        rs = parse(data)
        result_pats=[]
        # sinkers = Sinkers()
        for serial, r in enumerate(rs):
            type_name = r['type']
            theme = type_name.split('_')[0]
            # print(type_name)
            meta = build_meta(r, data)
            # print(f"meta keys {meta.keys()}")

            # mod_rs = langspecs.check_langspec(data['lang'], meta, r['domains'], type_name)
            # sinkers.add_module_results(mod_rs)

            # infers
            pats = []  # tuples list

            def do_infers(ctx:Context, ds, filters):
                from sagas.nlu.inspectors_dataset import get_interrogative
                if 'head' in r:
                    # $ se 'you are dead'  # true
                    # $ spt 'Com licença, onde é o banheiro?'  # false
                    logger.debug(f"head: {r['head']}, filter: {'head' in filters}")
                    rep = get_interrogative(r['head'], self.lang)
                    if rep:
                        pats.append((5, f"interr_root('{rep}')"))

                df = sagas.to_df(r['domains'], ['rel', 'index',
                                                'text', 'lemma',
                                                'children', 'features'])
                pat = self.proc_word(type_name, r['word'],
                                r['head'] if 'head' in r else '',
                                r['index'], r,
                                self.lang)
                pat['rels']=[sub[0] for sub in r['domains']]
                pat['stems']=self.stem_chunks(r)
                pat['ctx']=ctx

                domain=DomainToken(**pat)
                logger.debug(f".. proc word {r['word']}, "
                             f"verb in filter ({'[verb]' in filters}), "
                             f"predicate in filter ({'[predicate]' in filters}), "
                             f"stems: {domain.stems}")
                if '[verb]' not in filters and '[predicate]' not in filters:
                    self.induce_domain_from_exts(domain, 'verb', pats)

                pat_r = self.induce_pattern(domain, ds, verbose)
                parts = self.proc_children_column(df, self.lang)
                for part in parts:
                    # logger.debug(f"{part.name}: {part.word}")
                    if part.name not in filters:
                        part.domain=domain
                        self.induce_part(part, pats, type_name, verbose)
                # display_synsets(f"[{theme}]", meta, r, data['lang'])
                return pat_r

            # induce with wordnet
            ds = display_synsets(f"[{theme}]", meta, r, self.lang, collect=True)
            domains = r['domains']
            ctx = Context(meta, domains, name='_test_')
            pat_r = do_infers(ctx, ds, [el['indicator'] for el in ds])
            indicators = []
            for el in ds:
                if el['indicator'] not in indicators:
                    self.induce_spec(sagas.to_obj(el), pats, type_name)
                    indicators.append(el['indicator'])

            pats = sorted(pats, key=lambda pat: -pat[0])
            paras = ', '.join(p[1] for p in pats)
            if paras:
                result_pats.append(f"{pat_r}({paras}),")

            # debug
            if verbose:
                print('*', '-' * 45)
                pprint(ds)

        # sinkers.process_with_sinkers()
        return result_pats

# infers=Inferencer()

def do_infers(text:Text, source:Text) -> (Text, List[Text]):
    infers = Inferencer(source)
    pats = infers.infer(text)

    # generate cli command
    shortcuts = {'ja': 'sj', 'zh': 'sz'}
    cli_head = shortcuts[source] if source in shortcuts else f"s{source}"
    cli_cmd = f"# $ {cli_head} '{text}'"
    tc.emp('white', cli_cmd)

    for pat in pats:
        tc.emp('yellow', pat)
    return cli_cmd, pats

class InferencerCli(object):
    def infer(self, sents, lang='en', verbose=False):
        """
        $ python -m sagas.nlu.inferencer infer '水としょうゆを混ぜた。' ja
            pat(5, name='predict_mix').verb(specsof('*', 'mix'), ヲ=kindof('water', '*')),
        $ python -m sagas.nlu.inferencer infer 'Ellos ya leyeron ese libro en la escuela.' es
            pat(5, name='behave_read').verb(extract_for('plain', 'advmod'), behaveof('read', 'v'), nsubj=agency, obl=kindof('school', '*'), obj=kindof('book', '*')),
        $ python -m sagas.nlu.inferencer infer 'you are dead' en
            pat(5, name='desc_dead').cop(behaveof('dead', '*'), nsubj=agency, cop='c_aux'),
        $ python -m sagas.nlu.inferencer infer '予約を火曜日から木曜日に変えてもらった。' ja
        $ python -m sagas.nlu.inferencer infer ''太陽は月に比べて大きいです。' ja
        $ python -m sagas.nlu.inferencer infer 'Berapa umur kamu?' id # (en="How old are you?")
            pat(5, name='ana_age').root(behaveof('age', 'n')),
        $ python -m sagas.nlu.inferencer infer 'Apa yang lebih murah?' id # (What is cheaper?)
            pat(5, name='desc_abundant').cop(extract_for('plain', 'advmod'), behaveof('abundant', '*'), nsubj=agency, head_amod=interr('what')),

        :param sents:
        :param lang:
        :return:
        """
        infers = Inferencer(lang)
        return infers.infer(sents, verbose=verbose)

if __name__ == '__main__':
    from sagas.tool.loggers import init_logger
    import fire
    init_logger()
    # startup.start()
    fire.Fire(InferencerCli)

