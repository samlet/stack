from cachetools import cached

@cached(cache={})
def extract_entities(sents):
    import jieba.posseg as pseg
    words = pseg.cut(sents,use_paddle=True)
    tokens=[(word, flag) for word, flag in words]
    running_offset = 0
    rs = []
    for token in tokens:
        word = token[0]
        word_offset = sents.index(word, running_offset)
        word_len = len(word)
        running_offset = word_offset + word_len
        rs.append({"start": word_offset,
                   "end": running_offset,
                   'text': word,
                   'entity': token[1],
                   })
    return [w for w in rs if w['entity'] in {'PER', 'LOC', 'ORG', 'TIME'}]



