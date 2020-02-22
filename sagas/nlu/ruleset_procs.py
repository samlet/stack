from typing import Text, Dict

from sagas.nlu.corenlp_parser import get_chunks
from sagas.nlu.rules_meta import build_meta
from sagas.nlu.inspector_common import Inspector, Context, non_spaces
from sagas.conf.conf import cf
from sagas.nlu.uni_intf import SentenceIntf
from sagas.nlu.utils import fix_sents
from sagas.nlu.uni_remote import dep_parse, parse_and_cache
from sagas.nlu.uni_remote_viz import list_contrast, display_doc_deps
import sagas.tracker_fn as tc
import json_utils
from cachetools import cached
from pprint import pprint
import logging

logger = logging.getLogger(__name__)

def parse_sents(data: Dict):
    sents, source, engine=data['sents'], data['lang'], data['engine']
    sents=fix_sents(sents, source)
    # engine=cf.engine(source)
    return parse_and_cache(sents, source, engine)

@cached(cache={})
def cached_chunks(sents:Text, source:Text, engine:Text):
    doc, resp=parse_and_cache(sents, source, engine)
    return {'doc':doc,
            'predicts': resp['predicts'] if 'predicts' in resp else [],
            'verb_domains': get_verb_domain(doc),
            'root_domains': get_root_domain(doc),
            'aux_domains': get_aux_domain(doc),
            'subj_domains': get_subj_domain(doc),
            }

def root_predicate(doc:SentenceIntf, predicts):
    tag_id = doc.root.index - 1
    if predicts:
        for pred in predicts:
            idx=pred['index']
            if tag_id==idx:
                return pred
    return None

def get_main_domains(sents:Text, source:Text, engine:Text):
    chunks=cached_chunks(sents, source, engine)
    return next((e, chunks[e]) for e in ('predicts', 'verb_domains',
                                         'aux_domains', 'subj_domains',
                                         'root_domains') if len(chunks[e]) > 0)

equals = lambda a, b: str(a) == str(b)
def children(word, sent):
    return filter(lambda w: equals(w.governor, word.index), sent.words)

def extract(l, delim):
    keys = {x['dependency_relation'] for x in l}
    grp = lambda p, col: [x[col] for x in l if x['dependency_relation'] == p]
    text_chunks = {x: delim.join(grp(x, 'text')) for x in keys}
    lemma_chunks = {x: delim.join(grp(x, 'lemma')) for x in keys}
    rs = {}
    for e in l:
        e['text'] = text_chunks[e['dependency_relation']]
        e['lemma'] = lemma_chunks[e['dependency_relation']]
        rs[e['dependency_relation']] = e
    return rs


def group_by(l, field='dependency_relation'):
    keys = {x[field] for x in l}
    grp = lambda p: [x for x in l if x[field] == p]
    return {key: grp(key) for key in keys}


def get_verb_domain(sent):
    from sagas.nlu.uni_intf import sub_comps
    rs = []

    verbs = list(filter(lambda w: w.upos == "VERB", sent.words))
    if len(verbs) > 1:
        # filter the verbs which in clausal complement
        verbs = [word for word in verbs if word.dependency_relation not in sub_comps]
    for word in verbs:
        domains = []
        # stems = []
        for c in filter(lambda w: equals(w.governor, word.index), sent.words):
            c_domains = [w.ctx for w in children(c, sent)]
            domains.append({**c.ctx, **group_by(c_domains)})

        token = {**word.ctx, **group_by(domains)}
        # add governor as head domain
        if word.governor != 0:
            head = sent.words[word.governor - 1]
            token['head'] = head.ctx
        rs.append(token)
    return rs

def get_root_domain(sent_p):
    root = next(w for w in sent_p.words if w.dependency_relation in ('root', 'hed'))
    logger.debug(f"root: {root.index}, {root.text}({root.upos})")
    root_idx = int(root.index)
    domains = []
    # stems = []
    rs = []
    for word in (w for w in sent_p.words if w.governor == root_idx):
        # print(f"{__name__}: {word.dependency_relation}: {word.text}")
        logger.debug(f"{word.dependency_relation}: {word.text}")
        # add_domain(domains, stems, word, sent_p)
        c=word
        c_domains = [w.ctx for w in children(c, sent_p)]
        domains.append({**c.ctx, **group_by(c_domains)})

    word = root
    token = {**word.ctx, **group_by(domains)}
    rs.append(token)
    return rs

def build_token(sent, word, dc, domains):
    token = {**word.ctx, **group_by(domains)}
    # add_head(domains, dc, sent)
    if dc.governor != 0:
        head = sent.words[dc.governor - 1]
        token['head'] = head.ctx
    token['dc'] = dc.ctx
    return token

def get_aux_domain(sent):
    rs = []
    for word in filter(lambda w: w.upos == "AUX", sent.words):
        if word.governor == 0:
            # if the aux word is root; (这种情形会出现在德语依存分析中, 但在英语依存分析中是正常的)
            dc = word
        else:
            dc = sent.words[word.governor - 1]
        domains = []
        # 需要收集的是aux单词依赖的对象的关联集, 而不是aux单词自身的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            c_domains = [w.ctx for w in children(c, sent)]
            domains.append({**c.ctx, **group_by(c_domains)})

        token=build_token(sent, word, dc, domains)
        rs.append(token)
    return rs


def get_subj_domain(sent):
    rs = []
    for word in filter(lambda w: w.dependency_relation.endswith('subj'), sent.words):
        dc = sent.words[word.governor - 1]
        domains = []
        # 需要收集的是subj依赖的对象的关联集
        for c in filter(lambda w: equals(w.governor, dc.index), sent.words):
            c_domains = [w.ctx for w in children(c, sent)]
            domains.append({**c.ctx, **group_by(c_domains)})

        token = build_token(sent, word, dc, domains)
        rs.append(token)
    return rs

def print_root_domains(sents, lang, comps):
    # from pprint import pprint
    data = {'lang': lang, "sents": sents, 'engine': 'corenlp'}
    doc_jsonify, resp = parse_sents(data)
    domains = get_root_domain(doc_jsonify)
    # pprint(domains)

    ###
    root = domains[0]
    tc.emp('yellow', f"+ {root['lemma']}_{root['upos'].lower()}")
    for comp in comps:
        if comp in root:
            obj = root[comp][0]
            comps = []
            for k, c in obj.items():
                if isinstance(c, list):
                    comps.append((k, [f"{citem['lemma']}_{citem['upos'].lower()}" for citem in c]))
            comps_str = [f"{c[0]}:{','.join(c[1])}" for c in comps]
            tc.emp('yellow', f"\t☌ {comp}:{obj['lemma']}_{obj['upos'].lower()} {comps_str}")

def chains(word, lang, pos):
    from sagas.nlu.nlu_cli import get_chains
    resp = get_chains(word, lang, pos)
    if len(resp) > 0:
        return [', '.join(chain['chain']) for chain in resp]
    return []

def list_words(domains, lang, with_chains):
    top = '_'
    rs = []
    filters = ('pron', 'punct', 'part')

    # filters=()
    def get_words(domains, top):
        upos = domains['upos'].lower()
        word = domains['text']
        lemma = domains['lemma']
        # rel = domains['dependency_relation']
        key = f"{top}"
        if upos not in filters:
            word_f=f"{word}/{lemma}"
            if with_chains:
                pos='v' if upos=='verb' else '*'
                specs=chains(word_f, lang, pos)
            else:
                specs=[]
            rs.append({'ref': key, 'word':word, 'lemma':lemma, 'upos': upos, 'sepcs':specs})
        for k, v in domains.items():
            if isinstance(v, list):
                for child in v:
                    get_words(child, key + '/' + k)

    get_words(domains, top)
    return rs

def create_host():
    from durable.engine import Host
    import durable.lang as dlang

    host = Host()
    ruleset_definitions = {}
    for name, rset in dlang._rulesets.items():
        full_name, ruleset_definition = rset.define()
        ruleset_definitions[full_name] = ruleset_definition

    host.register_rulesets(ruleset_definitions)
    return host

class RulesetProcs(object):
    def __init__(self, verbose=True):
        self.verbose=verbose

    def print_sents(self, sents, lang, engine=None):
        """
        $ python -m sagas.nlu.ruleset_procs print_sents 'I want to play music.' en
        $ python -m sagas.nlu.ruleset_procs print_sents "クモは4つの右の目をしています。" ja corenlp

        :param sents:
        :param lang:
        :return:
        """
        # lang = 'en'
        if engine is None:
            engine=cf.engine(lang)
        data = {'lang': lang, "sents": sents, 'engine': engine}
        doc_jsonify, resp = parse_sents(data)
        rs = get_chunks(doc_jsonify)

        if lang in non_spaces:
            delim = ''
        else:
            delim = ' '
        for serial, r in enumerate(rs):
            meta = build_meta(r, data)
            domains = r['domains']
            # print([(x[0], x[2]) for x in domains])
            #
            keys = {x[0] for x in domains}
            grp = lambda p, idx: [x[idx] for x in domains if x[0] == p]
            tokens = {x: grp(x, 2) for x in keys}
            words = {x: delim.join(grp(x, 2)) for x in keys}
            lemmas = {x: delim.join(grp(x, 3)) for x in keys}
            print('meta keys', meta.keys())
            print('tokens', tokens)
            print('words', meta['word'], words)
            print('lemmas', lemmas)
            #
            ctx = Context(meta, domains)
            # print(ctx.lemmas)
            print('chunks', ctx._chunks)

        g = display_doc_deps(doc_jsonify, resp, translit_lang=lang)
        print(*[(w.index, w.text, w.governor, doc_jsonify.words[w.governor - 1].text) for w in doc_jsonify.words],
              sep='\n')
        tc.gv(g)

    def verbs(self, sents, lang='en', do_action=False):
        """
        单词的wordnet匹配使用专门的ruleset来评估, 匹配成功的rule会写入状态, 比如spec_xcomp_obj='music',
        此处的music对应knowledgebase的object_type.
        有效成分的单词wordnet引用依次放入ruleset评估, 这样会得到一个状态集, 这个状态集会放入句子结构,
        供sents_ruleset评估.
	    sents_ruleset会收集到多个intents保存到状态中, 遍历intents, 如果intent有action可触发,
	    则触发这个action.

        $ python -m sagas.nlu.ruleset_procs verbs 'I want to play music.' en
            ```
            [{'ref': 'want/want', 'upos': 'verb'},
             {'ref_xcomp': 'play/play', 'upos': 'verb'},
             {'ref_xcomp_obj': 'music/music', 'upos': 'noun'}]
            ```
        $ python -m sagas.nlu.ruleset_procs verbs 'I want to play video.' en
        $ python -m sagas.nlu.ruleset_procs verbs 'I would like to play video.' en
        $ python -m sagas.nlu.ruleset_procs verbs "i'd like to play sound." en
        $ verbs 'I want to play music.' en True

        :param sents:
        :param lang:
        :return:
        """
        import sagas.nlu.ruleset_fixtures as rf

        data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
        doc_jsonify, resp = parse_sents(data)
        v_domains=get_verb_domain(doc_jsonify)
        if self.verbose:
            tc.gv(display_doc_deps(doc_jsonify, resp))
            pprint(v_domains)
            json_utils.write_json_to_file('./out/v_domain.json', v_domains[0])

            # list words
            tc.emp('cyan', f"✁ list words. {'-' * 25}")

        intents=[]
        host = create_host()
        for d in v_domains:
            tokens=list_words(d, lang, with_chains=True)
            if self.verbose:
                pprint(tokens)

            # specs evaluate
            tc.emp('cyan', f"✁ specs evaluate. {'-' * 25}")
            r3={}
            for token in tokens:
                r3 = host.assert_fact('chains', token)
                pprint(r3) # the last result is all state
            [r3.pop(key) for key in ['$s', 'id', 'sid']]
            tc.emp('red', f"specs state - {r3}")

            # sents evaluate
            tc.emp('cyan', f"✁ sents evaluate. {'-' * 25}")
            sents_data={**d, **r3}
            tc.emp('cyan', f"  keys: {', '.join(sents_data.keys())}")
            result=host.assert_fact('sents', sents_data)
            tc.emp('red', f"sents state - {result}")
            if 'intents' in result:
                intents.extend(result['intents'])

        self.process_intents(sents, lang, intents, do_action)

    def process_intents(self, sents, lang, intents, do_action:bool):
        from sagas.nlu.ruleset_actions import ruleset_actions

        print('intents: ', intents)
        action_binds = ruleset_actions.get_intents()
        if self.verbose:
            pprint(action_binds)
        schedules = []
        for intent_item in intents:
            intent = intent_item['intent']
            acts = [ac['action'] for ac in action_binds if ac['intent'] == intent]

            tc.emp('green', f"action for intent {intent}: {acts}")
            if len(acts) > 0:
                schedules.append({'intent': intent, 'action': acts,
                                  'sents': sents, 'lang': lang,
                                  'object_type': intent_item['object_type'],
                                  'parameters': {},
                                  })
        if len(schedules) > 0:
            self.invoke_actions(schedules, do_action)
        else:
            tc.emp("yellow", 'no scheduled actions.')

    def invoke_actions(self, schedules, do_action):
        import requests
        import json
        print('schedules:', schedules, ', do action:', do_action)
        if do_action:
            for ac in schedules:
                values={"object_type": ac["object_type"],
                        "sents":ac["sents"],
                        'parameters': ac['parameters']}
                values_str=json.dumps(values, ensure_ascii=False)
                # text = f'/{ac["intent"]}{{"object_type": "{ac["object_type"]}", "sents":"{ac["sents"]}"}}'
                text = f'/{ac["intent"]}{values_str}'
                data = {'mod': 'genesis', 'lang': ac['lang'], "sents": text}
                response = requests.post(f'{cf.ensure("agents_servant")}/message/my', json=data)
                print('status code:', response.status_code)
                pprint(response.json())

    def invoke_testing(self):
        """
        $ python -m sagas.nlu.ruleset_procs invoke_testing

        :return:
        """
        schedules= [{'intent': 'perform_media',
                     'object_type': 'testing',
                     'action': ['action_perform_sound'],
                     'sents': 'I want to play music.',
                     'parameters': {
                        'media_list': ['first song', 'second song'],
                        'media_type': 'sound'},
                     'lang': 'en'}]
        self.invoke_actions(schedules, True)

    def asserts(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.ruleset_procs asserts 'I want to play music.' en

        :param sents:
        :param lang:
        :return:
        """
        import sagas.nlu.ruleset_fixtures as rf

        data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
        doc_jsonify, resp = parse_sents(data)
        v_domains = get_verb_domain(doc_jsonify)

        host = create_host()
        for v in v_domains:
            r1 = host.assert_fact('verbs', v)
            pprint(r1)

    def assert_chains(self, word, lang='en', pos='n'):
        """
        $ python -m sagas.nlu.ruleset_procs assert_chains world en n

        :param word:
        :return:
        """
        import sagas.nlu.ruleset_fixtures as rf

        word_chains = chains(word, lang, pos)
        print(*word_chains, sep='\n')

        host = create_host()
        r3 = host.assert_fact('chains', {'word': word, 'amod': word_chains})
        pprint(r3)

if __name__ == '__main__':
    import fire
    from sagas.tool.loggers import init_logger
    init_logger()
    fire.Fire(RulesetProcs)
