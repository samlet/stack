class Token(object):
    def __init__(self, index, word, word_offset, positions):
        self.index = index
        self.word = word
        self.word_offset = word_offset
        self.positions = positions

    def __str__(self):
        return '%s %s' % (self.word, self.positions)


def tokenize(text, sent):
    running_offset = 0
    tokens = []
    positions = []

    for doc_word in sent.words:
        word = doc_word.text
        word_offset = text.index(word, running_offset)
        word_len = len(word)
        running_offset = word_offset + word_len
        tokens.append(Token(doc_word.index, word, word_offset, {"start": word_offset, "end": running_offset}))
    return tokens

def in_range(element, container):
    return element[0]>=container[0] and element[1]<=container[1]

def get_included_entities(word_range, ent_pos):
    rs = []
    for ent in ent_pos:
        if in_range((ent['start'], ent['end']), word_range):
            rs.append(ent)
    return rs

def equals(a, b):
    return str(a) == str(b)

# def get_children(sent, word, rs):
#     for c in filter(lambda w: equals(w.governor, word.index), sent.words):
#         rs.append((c.index, c.text))
#         get_children(sent, c, rs)

def get_children_list(sent, word, include_self=True):
    from sagas.nlu.corenlp_parser import get_children
    rs = []
    get_children(sent, word, rs)
    if include_self:
        rs.append((word.index, word.text))
    # sort by word's index
    rs=sorted(rs, key=lambda _: int(_[0]))
    result = [w[1] for w in rs]
    positions=[int(w[0]) for w in rs]
    # if include_self:
    #     result.append(word.text)
    return result, positions

def get_word_features(word):
    # 'c' represent a chunk
    return ['c_{}_{}'.format(word.lemma, word.upos).lower()]

class ChunkEntitiesProcs(object):
    def __init__(self, lang='en'):
        from sagas.nlu.corenlp_helper import get_nlp

        self.lang=lang
        # spacy_model=lang_spacy_mappings[lang][0]
        # self.spacy_nlp=spacy.load(spacy_model)
        self.core_nlp=get_nlp(lang)

    def spacy_doc(self, sents, lang):
        from sagas.nlu.spacy_helper import spacy_mgr
        spacy_nlp = spacy_mgr.get_model(lang)
        return spacy_nlp(sents)

    # document level
    def entity_df(self, sents, lang):
        import sagas
        # from sagas.nlu.spacy_helper import spacy_mgr
        # spacy_nlp=spacy_mgr.get_model(lang)
        doc = self.spacy_doc(sents, lang)
        rs = []
        for ent in doc.ents:
            rs.append((ent.text, ent.start_char, ent.end_char, ent.label_))
        return sagas.to_df(rs, ['word', 'start', 'end', 'entity'])

    # token level
    def token_entity_df(self, sents, lang):
        import sagas
        doc = self.spacy_doc(sents, lang)
        rs = []
        for ent in doc:
            rs.append((ent.i, ent.idx, ent.text, ent.ent_type_, ent.ent_iob_,
                       [ent.is_punct, ent.like_num]))
        return sagas.to_df(rs, ['index', 'position', 'word', 'entity', 'iob', 'feat'])

    def entity_positions(self, sents, lang):
        doc = self.spacy_doc(sents, lang)
        rs = []
        for ent in doc.ents:
            rs.append({'text': ent.text, 'start': ent.start_char, 'end': ent.end_char, 'entity': ent.label_})
        return rs

    def get_verb_domain(self, sent):
        rs = []
        for word in filter(lambda w: w.upos == "VERB", sent.words):
            domains = []
            for c in filter(lambda w: equals(w.governor, word.index), sent.words):
                # print('\t', c.index, c.text, get_children_list(sent, c))
                children, positions = get_children_list(sent, c)
                domains.append((c.dependency_relation, c.index, c.text,
                                children, positions, get_word_features(c)))
            rs.append({'type': 'verb_domains', 'verb': word.text, 'index': word.index,
                       'domains': domains})
        return rs

    def get_chunks(self, sent):
        from sagas.nlu.corenlp_parser import get_chunks
        return get_chunks(sent)

    def list_chunk_entities(self, sents, lang='en'):
        """
        $ python -m sagas.nlu.chunk_entities list_chunk_entities 'Apple is looking at buying U.K. startup for $1 billion.'
        $ python -m sagas.nlu.chunk_entities list_chunk_entities "Where's the president?"
        $ python -m sagas.nlu.chunk_entities list_chunk_entities "διαμένω στη Νέα Υόρκη" el

        :param sents:
        :return:
        """
        import sagas

        doc = self.core_nlp(sents)
        doc_s = doc.sentences[0]

        tokens = tokenize(sents, doc_s)
        for tok in tokens:
            print(tok.index, '\t', tok.word, tok.word_offset, tok.positions)
        ent_pos = self.entity_positions(sents, lang)
        print(ent_pos)
        # process spans and overlaps
        chunks = []
        r = self.get_verb_domain(doc.sentences[0])
        # r = self.get_chunks(doc.sentences[0])
        if len(r)>0:
            for el in r[0]['domains']:
                span_id = el[0]
                span_pos = el[4]
                start_mark = tokens[span_pos[0] - 1]
                end_mark = tokens[span_pos[-1] - 1]
                word_range = [start_mark.positions['start'], end_mark.positions['end']]
                entities = get_included_entities(word_range, ent_pos)
                chunks.append((span_id, span_pos, word_range,
                               sents[word_range[0]:word_range[1]],
                               [ent['entity'] for ent in entities]
                               ))
            df = sagas.to_df(chunks, ['rel', 'positions', 'range', 'chunk text', 'entities'])
            sagas.print_df(df[['rel', 'chunk text', 'entities']])
        else:
            # print("no chunks.")
            print("no verbs.")

if __name__ == '__main__':
    import fire
    fire.Fire(ChunkEntitiesProcs)
