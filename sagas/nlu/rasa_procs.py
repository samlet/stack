from typing import Text
import requests
import logging
import json

from cachetools import cached, TTLCache

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

class RasaProcs(object):
    def testing_de(self, sents):
        """
        $ python -m sagas.nlu.rasa_procs testing_de "Shenzhen ist das Silicon Valley für Hardware-Firmen"
        :param sents:
        :return:
        """
        from sagas.conf.conf import cf
        # endpoint = "http://localhost:5000"
        endpoint = cf.ensure('nlu_multilang_servant')
        print('.. with endpoing', endpoint)
        result = invoke_nlu(endpoint, "de", "current", sents)
        if result != None:
            print(json.dumps(result, indent=4))
            intent=result["intent"]
            print('%s -> %f'%(intent['name'], intent['confidence']))
            entities=result['entities']
            print([ent['entity'] for ent in entities])

if __name__ == '__main__':
    import fire
    fire.Fire(RasaProcs)


