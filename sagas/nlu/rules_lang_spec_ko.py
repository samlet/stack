from typing import Text, Dict, Any

from sagas.nlu.rules_header import *
from sagas.nlu.inspector_common import Context
import sagas.tracker_fn as tc
import logging

logger = logging.getLogger(__name__)

def extract_ko(target, word):
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

def extract_nouns(key:Text, ctx:Context):
    # rs=extract_ko('nouns', ctx.words[key])
    rs = extract_ko('nouns', ctx.get_single_chunk_text(key))
    if rs:
        ctx.add_result('cust', 'nouns', key, rs)
        return True
    return False

class Rules_ko(LangSpecBase):
    @staticmethod
    def prepare(meta: Dict[Text, Any]):
        tc.emp('yellow', '.. Rules_ko prepare phrase')

    def verb_rules(self):
        pat, actions_obj = (self.pat, self.actions_obj)

        # $ sko '우리는 피자와 스파게티가 필요해요.'  (We need pizza and spaghetti.)
        # $ sko '우리는 생선과 스테이크가 필요해요.'  (We need fish and steaks.)
        self.collect(pats=[
            pat(-5, name='desc_need').verb(
                behaveof('need', '*', extract=extract_verb),
                checker(has_rel='nsubj'),
                nsubj=cust(extract_nouns),),
        ])
    

