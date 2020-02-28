from typing import Text, Dict, Any

from cachetools import cached

from sagas.nlu.rules_header import *
from sagas.nlu.inspector_common import Context
import sagas.tracker_fn as tc
import logging

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

def extract_verb(key:Text, ctx:Context):
    # word=ctx.words[key]
    word=key
    rs = extract_ko('pos', word)
    if rs:
        # print('******', rs[0][0])
        return rs[0][0]
    return word

def extract_noun_chunk(key:Text, ctx:Context):
    rs = extract_ko('nouns', ctx.get_single_chunk_text(key))
    if rs:
        return rs[0]['text']
    return ctx.words[key]

def extract_nouns(key:Text, ctx:Context):
    # rs=extract_ko('nouns', ctx.words[key])
    rs = extract_ko('nouns', ctx.get_single_chunk_text(key))
    if rs:
        ctx.add_result('cust', 'nouns', key, rs)
        return True
    return False

def extract_datetime(key:Text, ctx:Context):
    from sagas.nlu.content_representers import cnt_repr
    rs=cnt_repr.parse_snips(ctx.get_single_chunk_text(key), 'ko')
    if rs:
        ctx.add_result('cust', 'datetime', key, rs)
        return True
    return False

class Rules_ko(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ko prepare phrase')

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
        ])
    

