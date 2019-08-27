def dep_parse(sents, lang='en', engine='corenlp'):
    import requests
    import json
    from sagas.conf.conf import cf
    from sagas.nlu.uni_jsonifier import JsonifySentImpl

    data = {'lang': lang, "sents": sents, 'engine': engine}
    print(f".. request is {data}")
    response = requests.post(f'{cf.servant(engine)}/dep_parse', json=data)
    words = response.json()
    if len(words) == 0:
        print('.. dep_parse servant returns empty set.')
        print('.. request data is', data)
        return

    doc_jsonify = JsonifySentImpl(words)
    return doc_jsonify

