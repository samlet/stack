import stanfordnlp.server as corenlp

def test_tokensregex(corenlp_client, props, text):
    pattern = '([ner: PERSON]+) /wrote/ /an?/ []{0,3} /sentence|article/'
    matches = corenlp_client.tokensregex(text, pattern,
                                         annotators=props['annotators'],
                                         properties=props)
    print(matches)
    assert len(matches["sentences"]) == 1
    assert matches["sentences"][0]["length"] == 1
    assert matches == {
        "sentences": [{
            "0": {
                "text": "Chris wrote a simple sentence",
                "begin": 0,
                "end": 5,
                "1": {
                    "text": "Chris",
                    "begin": 0,
                    "end": 1
                }},
            "length": 1
        }, ]}


def test_semgrex(corenlp_client, props, text):
    pattern = '{word:wrote} >nsubj {}=subject >dobj {}=object'
    matches = corenlp_client.semgrex(text, pattern, to_words=True,
                                     annotators=props['annotators'],
                                     properties=props)
    print(matches)
    assert matches == [
        {
            "text": "wrote",
            "begin": 1,
            "end": 2,
            "$subject": {
                "text": "Chris",
                "begin": 0,
                "end": 1
            },
            "$object": {
                "text": "sentence",
                "begin": 4,
                "end": 5
            },
            "sentence": 0, }]

if __name__ == '__main__':
    sc = corenlp.CoreNLPClient(start_server=False, endpoint="http://localhost:9005")
    properties_key = 'english'
    props = {'pipelineLanguage': properties_key.lower(),
             'annotators': 'tokenize,ssplit,pos,depparse,lemma,natlog,ner,openie',
             'outputFormat': 'text'
             }
    test_tokensregex(sc, props, "Chris wrote a simple sentence that he parsed with Stanford CoreNLP.\n")
    test_semgrex(sc, props, "Chris wrote a simple sentence that he parsed with Stanford CoreNLP.")
