#!/usr/bin/env python
import requests
import fire
import logging
import json

logger = logging.getLogger(__name__)

#$ query.py query "can i get chinese food"
#$ ./query.py query "goodbye"
def query(a_str):
    # data = {'q':a_str, 'project':'nlu', 'model':'current'}
    data = '"q":"{}", "project":"nlu", "model":"current"'.format(a_str)
    response = requests.post('http://localhost:5000/parse', data="{"+data+"}")
    print(response.text)

#$ ./query.py talk "hi"
#$ ./query.py talk "/joke"
def talk(a_str):
    headers = {
        'content-type': 'application/json',
    }
    data = '{'+'"message": "{}"'.format(a_str)+'}'
    response = requests.post('http://localhost:5005/webhooks/rest/webhook', headers=headers, data=data)
    print(response.text)

# endpoint: http://localhost:5000
def invoke_nlu(endpoint, project_name, model_name, text):
    params = {
        "model": model_name,
        "project": project_name,
        "q": text
    }
    url = "{}/parse".format(endpoint)
    try:
        result = requests.get(url, params=params)
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

def test_nlu():
    endpoint= "http://localhost:5000"
    result=invoke_nlu(endpoint, "nlu", "current", "hi")
    if result != None:
        print(json.dumps(result, indent=4))

if __name__ == '__main__':
    fire.Fire()


