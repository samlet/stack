from cachetools import cached, TTLCache


def ltp_parse(sentence):
    from sagas.zh.ltp_procs import ltp

    words = ltp.segmentor.segment(sentence)
    postags = ltp.postagger.postag(words)
    arcs = ltp.parser.parse(words, postags)
    roles = ltp.labeller.label(words, postags, arcs)
    netags = ltp.recognizer.recognize(words, postags)

    rs = []
    for i in range(len(words)):
        pos = postags[i]
        dep_idx = int(arcs[i].head) - 1
        head = words[dep_idx]
        rel = arcs[i].relation
        ne = netags[i]
        rs.append({'head': head, 'text': words[i],
                   'rel': rel, 'pos': pos, 'entity': ne})

    return rs


@cached(cache=TTLCache(maxsize=1024*768, ttl=600))
def ltp_ner(sents):
    running_offset = 0
    rs = []
    tokens = ltp_parse(sents)
    for token in tokens:
        word = token['text']
        word_offset = sents.index(word, running_offset)
        word_len = len(word)
        running_offset = word_offset + word_len
        rs.append({"start": word_offset,
                   "end": running_offset,
                   'text': word,
                   'entity': token['entity']
                   })
    return [w for w in rs if w['entity'] != 'O']

