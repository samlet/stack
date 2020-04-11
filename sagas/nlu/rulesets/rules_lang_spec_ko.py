from typing import Text, Dict, Any

from cachetools import cached

from sagas.nlu.inferencer import extensions, DomainToken, InferPart
from sagas.nlu.rules_header import *
from sagas.nlu.inspector_common import Context
import sagas.tracker_fn as tc
import logging

from sagas.nlu.utils import get_possible_mean

logger = logging.getLogger(__name__)

@cached(cache={})
def extract_ko(target:Text, word:Text):
    import requests
    response = requests.post(f'http://localhost:1700/ko/extract/{target}',
                             json={'sents':word})
    if response.status_code == 200:
        sets= response.json()
        return sets
    return []

def extract_verb(key:Text, ctx:Context=None):
    # word=ctx.words[key]
    word=key
    rs = extract_ko('pos', word)
    if rs:
        # print('******', rs[0][0])
        return rs[0][0] # 第1个元素是动词原形
    return word

def extract_noun_chunk(key:Text, ctx:Context):
    rs = extract_ko('nouns', ctx.get_single_chunk_text(key))
    if rs:
        # return rs[0]['text']
        # 任意一个名词块符合条件即可, 所以用'/'串接
        return '/'.join([w['text'] for w in rs])
    return ctx.words[key]

def extract_nouns(key:Text, ctx:Context, check_fn) -> bool:
    # rs=extract_ko('nouns', ctx.words[key])
    rs = extract_ko('nouns', ctx.get_single_chunk_text(key))
    if rs:
        ctx.add_result('cust', 'nouns', key, rs)
        return True
    return False

def extract_datetime(key:Text, ctx:Context, check_fn):
    from sagas.nlu.content_representers import cnt_repr
    rs=cnt_repr.parse_snips(ctx.get_single_chunk_text(key), 'ko')
    if rs:
        ctx.add_result('cust', 'datetime', key, rs)
        return True
    return False

def get_nouns_spec(c:InferPart, part:Text):
    rs = extract_ko('nouns', c.text)
    if rs:
        last_spec=[r['spec'] for r in rs if 'spec' in r]
        if last_spec:
            spec=last_spec[-1].split('.')[0]
            return 2, f"{part}=kindof('{spec}', '*', extract=extract_noun_chunk)"
    return 4, f"extract_for('plain', '{part}')"

def get_verb_spec(c:DomainToken, part:Text):
    from sagas.nlu.nlu_cli import retrieve_word_info
    # rs = retrieve_word_info('get_synsets', f"{c.text}/{c.lemma}", 'ko', '*')
    word=extract_verb(c.text)
    rs = retrieve_word_info('get_synsets', word, 'ko', '*')
    # print('.. ', c.text, rs)
    mean=get_possible_mean(rs)
    if mean:
        return 4, f"behaveof('{mean}', '*', extract=extract_verb)"
    return None

def get_verb_interr(c:DomainToken, part:Text):
    from sagas.nlu.inspectors_dataset import get_interrogative
    from sagas.nlu.transliterations import translits
    word=translits.translit(c.text.split('/')[0], 'ko')
    rep=get_interrogative(word, 'ko')
    if rep:
        return 4, f"interr_root('{rep}')"
    else:
        return 4, "interr_root('??')"

extensions.register_parts('ko',{
    'nsubj': lambda c,t: [(4, "extract_for('plain', 'nsubj')"),
                          (2, "nsubj=agency")],
    'obl': lambda c,t: get_nouns_spec(c, 'obl'),
})
extensions.register_domains('ko',{
    # Testcases:
    # $ sko '우리는 피자와 스파게티가 필요해요.'   -> spec
    # $ sko '이번 주말에 벌써 계획이 있어요?'     -> interr_root
    'verb': lambda c,t: get_verb_spec(c, t) or get_verb_interr(c,t),
})

class Rules_ko(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ko(Korean, 韩语) prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        self.collect(pats=[
            # $ python -m sagas.ko.ko_helper nouns '피자와 스파게티가'
            # $ sko '우리는 피자와 스파게티가 필요해요.'  (We need pizza and spaghetti.)
            # $ sko '우리는 생선과 스테이크가 필요해요.'  (We need fish and steaks.)
            pat(-5, name='desc_need').verb(
                behaveof('need', '*', extract=extract_verb),
                checker(has_rel='nsubj'),
                nsubj=cust(extract_nouns),),

            # $ sko '이번 주말에 벌써 계획이 있어요?'
            #   (Do you already have plans for this weekend?)
            #   (ibeon jumal-e beolsseo gyehoeg-i iss-eoyo?)
            pat(-5, name='desc_plan').verb(
                interr_root('have'),
                checker(has_rel='obl'),
                obl=cust(extract_datetime),
                nsubj=kindof('plan', '*', extract=extract_noun_chunk), ),

            # $ sko '우리 산에 갈까요?'
            #   (Shall we go to the mountains?)
            #   (uli san-e galkkayo?)
            # $ sko '우리 해변에 갈까요?'  (Shall we go to the beach?)
            pat(5, name='act_geo').verb(
                interr_root('act'),
                checker(has_rel='obl'),
                obl=kindof('geological_formation', 'n', extract=extract_noun_chunk), ),
        ])
    

