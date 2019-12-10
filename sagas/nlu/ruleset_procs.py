from sagas.nlu.corenlp_parser import get_chunks
from sagas.nlu.rules_meta import build_meta
from sagas.nlu.inspector_common import Inspector, Context, non_spaces
from sagas.conf.conf import cf
from sagas.nlu.utils import fix_sents
from sagas.nlu.uni_remote import dep_parse
from sagas.nlu.uni_remote_viz import list_contrast, display_doc_deps
import sagas.tracker_fn as tc
import json_utils
from pprint import pprint

def parse_sents(data):
    sents, source=data['sents'], data['lang']
    sents=fix_sents(sents, source)
    engine=cf.engine(source)
    doc_jsonify, resp = dep_parse(sents, source, engine, ['predicts'])
    return doc_jsonify, resp


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
        stems = []
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
    def print_sents(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.ruleset_procs print_sents 'I want to play music.' en
        :param sents:
        :param lang:
        :return:
        """
        # lang = 'en'
        data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
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

        g = display_doc_deps(doc_jsonify, resp)
        print(*[(w.index, w.text, w.governor, doc_jsonify.words[w.governor - 1].text) for w in doc_jsonify.words],
              sep='\n')
        tc.gv(g)

    def verbs(self, sents, lang='en', do_action=False):
        """
        $ python -m sagas.nlu.ruleset_procs verbs 'I want to play music.' en
            ```
            [{'ref': 'want/want', 'upos': 'verb'},
             {'ref_xcomp': 'play/play', 'upos': 'verb'},
             {'ref_xcomp_obj': 'music/music', 'upos': 'noun'}]
            ```
        $ python -m sagas.nlu.ruleset_procs verbs 'I want to play video.' en

        :param sents:
        :param lang:
        :return:
        """
        import sagas.nlu.ruleset_fixtures as rf
        from sagas.nlu.ruleset_actions import ruleset_actions

        data = {'lang': lang, "sents": sents, 'engine': cf.engine(lang)}
        doc_jsonify, resp = parse_sents(data)
        v_domains=get_verb_domain(doc_jsonify)
        pprint(v_domains)
        json_utils.write_json_to_file('./out/v_domain.json', v_domains[0])

        # list words
        tc.emp('cyan', f"✁ list words. {'-' * 25}")

        intents=[]
        host = create_host()
        for d in v_domains:
            tokens=list_words(d, lang, with_chains=True)
            pprint(tokens)

            tc.emp('cyan', f"✁ specs evaluate. {'-' * 25}")
            r3={}
            for token in tokens:
                r3 = host.assert_fact('chains', token)
                pprint(r3) # the last result is all state
            [r3.pop(key) for key in ['$s', 'id', 'sid']]
            tc.emp('red', f"specs state - {r3}")

            tc.emp('cyan', f"✁ sents evaluate. {'-' * 25}")
            sents_data={**d, **r3}
            tc.emp('cyan', f"  keys: {', '.join(sents_data.keys())}")
            result=host.assert_fact('sents', sents_data)
            tc.emp('red', f"sents state - {result}")
            if 'intents' in result:
                intents.extend(result['intents'])

        print('intents: ', intents)
        action_binds=ruleset_actions.get_intents()
        pprint(action_binds)
        schedules=[]
        for intent in intents:
            acts=[ac['action'] for ac in action_binds if ac['intent']==intent]
            tc.emp('green', f"action for intent {intent}: {acts}")
            schedules.append({'intent': intent, 'action': acts,
                              'sents': sents, 'lang': lang
                              })

        self.invoke_actions(schedules, do_action)

    def invoke_actions(self, schedules, do_action):
        import requests
        print('schedules:', schedules, ', do action:', do_action)
        if do_action:
            for ac in schedules:
                text = f'/{ac["intent"]}{"object_type": "sents", "sents":"{ac["sents"]}"}'
                data = {'mod': 'genesis', 'lang': ac['lang'], "sents": text}
                response = requests.post(f'http://localhost:18099/message/my', json=data)
                print('status code:', response.status_code)
                pprint(response.json())

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
    fire.Fire(RulesetProcs)
