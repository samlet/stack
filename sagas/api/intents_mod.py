from durable.lang import assert_fact
from sagas.nlu.ruleset_procs import list_words, cached_chunks
from sagas.nlu.ruleset_actions import ruleset_actions
from sanic import Blueprint
from sanic.response import json
import requests
from sagas.conf.conf import cf
import logging

from sagas.tool.loggers import init_logger
from sagas.nlu.ruleset_registry import *

logger = logging.getLogger(__name__)

intents_mod = Blueprint('intents', url_prefix='/intents')

def get_intents(domains, lang):

    intents = []

    for d in domains:
        tokens = list_words(d, lang, with_chains=True)

        # specs evaluate
        # tc.emp('cyan', f"✁ specs evaluate. {'-' * 25}")
        r3 = {}
        for token in tokens:
            r3 = assert_fact('chains', token)
            logger.debug(r3)  # the last result is all state
        [r3.pop(key) for key in ['$s', 'id', 'sid']]

        # sents evaluate
        sents_data = {**d, **r3}
        logger.debug(f"  keys: {', '.join(sents_data.keys())}")
        result = assert_fact('sents', sents_data)
        # tc.emp('red', f"sents state - {result}")
        if 'intents' in result:
            intents.extend(result['intents'])

    return intents

def get_schedules(sents, lang, intents):
    action_binds = ruleset_actions.get_intents()
    schedules = []
    for intent_item in intents:
        intent = intent_item['intent']
        acts = [ac['action'] for ac in action_binds if ac['intent'] == intent]

        # tc.emp('green', f"action for intent {intent}: {acts}")
        if len(acts) > 0:
            schedules.append({'intent': intent, 'action': acts,
                              'sents': sents, 'lang': lang,
                              'object_type': intent_item['object_type'],
                              'parameters': {},
                              })
    return schedules

def comm(schedules):
    import json
    rs=[]
    for ac in schedules:
        values={"object_type": ac["object_type"],
                "sents":ac["sents"],
                'parameters': ac['parameters']}
        values_str=json.dumps(values, ensure_ascii=False)
        # text = f'/{ac["intent"]}{{"object_type": "{ac["object_type"]}", "sents":"{ac["sents"]}"}}'
        text = f'/{ac["intent"]}{values_str}'
        data = {'mod': 'genesis', 'lang': ac['lang'], "sents": text}
        response = requests.post(f'{cf.ensure("agents_servant")}/message/my', json=data)
        # print('status code:', response.status_code)
        if response.status_code==200:
            rs.append(response.json())
        else:
            logger.error(f"action {ac} return code {response.status_code}")
    return rs

@intents_mod.post('/comm')
def handle_comm(request):
    rd = request.json
    schedules=rd['schedules']  # parameter
    return json(comm(schedules))

def request_intents(sents, lang, domain):
    chunks = cached_chunks(sents, lang, cf.engine(lang))
    domains = chunks[domain]
    return get_intents(domains, lang)

@intents_mod.post('/retrieve/<domain>/<lang>')
async def handle_intents(request, domain, lang):
    """
    $ curl -d '{"sents":"I want to play music."}' \
        -H "Content-Type: application/json" -X POST \
        localhost:1700/intents/retrieve/verb_domains/en | json
    :param request:
    :param domain:
    :param lang:
    :return:
    """
    rd = request.json
    sents=rd['sents']
    return json(request_intents(sents, lang, domain))

@intents_mod.post('/schedules/<lang>')
async def handle_schedules(request, lang):
    rd = request.json
    sents=rd['sents']       # parameter
    intents=rd['intents']   # parameter
    schedules=get_schedules(sents, lang, intents)
    return json(schedules)

class IntentsMod(object):
    def behave(self, sents, lang='en', domain='verb_domains'):
        """
        $ python -m sagas.api.intents_mod behave 'I want to play music'
        :param sents:
        :param lang:
        :param domain:
        :return:
        """
        from pprint import pprint

        intents=request_intents(sents, lang, domain)
        print(f".. intents: {intents}")
        schedules = get_schedules(sents, lang, intents)
        print(f".. schedules: {schedules}")
        rs=comm(schedules)
        print(".. agent response:")
        pprint(rs)

if __name__ == '__main__':
    import fire
    init_logger()
    fire.Fire(IntentsMod)

