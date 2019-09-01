def dep_parse(sents, lang='en', engine='corenlp', pipelines=None):
    import requests
    import json
    from sagas.conf.conf import cf
    from sagas.nlu.uni_jsonifier import JsonifySentImpl

    if pipelines is None:
        pipelines = []
    data = {'lang': lang, "sents": sents, 'engine': engine, 'pipelines':pipelines}
    print(f".. request is {data}")
    response = requests.post(f'{cf.servant(engine)}/dep_parse', json=data)
    if response.status_code != 200:
        print('.. dep_parse servant invoke fail.')
        return None, None

    result = response.json()
    words=result['sents']
    if len(words) == 0:
        print('.. dep_parse servant returns empty set.')
        print('.. request data is', data)
        return None, None

    doc_jsonify = JsonifySentImpl(words)
    if len(pipelines)>0:
        result_set={p:result[p] for p in pipelines}
        return doc_jsonify, result_set
    return doc_jsonify, None

