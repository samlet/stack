from typing import Text, Any, Dict, List, Union, Optional
import requests
import logging
import json
from sagas.conf.conf import cf
from cachetools import cached, TTLCache
from sagas.nlu.intf import Entity

logger = logging.getLogger(__name__)

@cached(cache=TTLCache(maxsize=1024, ttl=600))
def invoke_nlu(endpoint:Text, project_name:Text, model_name:Text, text:Text):
    params = {
        "model": model_name,
        "project": project_name,
        "q": text
    }
    url = "{}/parse".format(endpoint)
    try:
        # result = requests.get(url, params=params)
        result = requests.post(url, json=params)
        if result.status_code == 200:
            return result.json()
        else:
            logger.error(
                "Failed to parse text '{}' using rasa NLU over http. "
                "Error: {}".format(text, result.text))
            return None
    except Exception as e:
        logger.error(
            "Failed to parse text '{}' using rasa NLU over http. "
            "Error: {}".format(text, e))
        return None

def rasa_nlu_parse(sents:Text, host_and_port:Text='http://localhost:5005') -> Dict[Text, Any]:
    response = requests.post(f'{host_and_port}/model/parse', json={'text': sents})
    if response.status_code!=200:
        logger.warning(f'status code is {response.status_code}, fail to parse {sents}')
        return {}
    return response.json()

def get_entities(sents:Text, rasa_entry='rasa_default'):
    """
    Start rasa service: simple/rasa-serv.sh
    >>> from sagas.nlu.rasa_procs import get_entities
    >>> get_entities('id like to find an expensive restaurant', 'rasa_simple')
        [Entity(start=19, end=28, extractor='CRFEntityExtractor', value='hi', entity='price', confidence=0.930441018)]

    :param sents:
    :param rasa_entry:
    :return:
    """
    result = rasa_nlu_parse(sents, cf.ensure(rasa_entry))
    ents = result['entities'] if result and 'entities' in result else []
    return [Entity.from_dict(e) for e in ents]

class RasaProcs(object):
    def parse(self, sents, lang):
        """
        $ python -m sagas.nlu.rasa_procs parse "Shenzhen ist das Silicon Valley für Hardware-Firmen" de
        $ python -m sagas.nlu.rasa_procs parse 'what restaurants can you recommend?' en

        :param sents:
        :return:
        """
        from sagas.conf.conf import cf
        # endpoint = "http://localhost:5000"
        endpoint = cf.ensure('nlu_multilang_servant')
        print('.. with endpoing', endpoint)
        result = invoke_nlu(endpoint, lang, "current", sents)
        if result != None:
            print(json.dumps(result, indent=4))
            intent=result["intent"]
            print('%s -> %f'%(intent['name'], intent['confidence']))
            entities=result['entities']
            print([ent['entity'] for ent in entities])

if __name__ == '__main__':
    import fire
    fire.Fire(RasaProcs)


