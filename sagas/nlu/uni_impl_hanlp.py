from sagas.nlu.uni_intf import RootWordImpl, WordIntf, SentenceIntf

upos_maps={'a':'ADJ', 'p':'ADP', 'd':'ADV',
           'u':'AUX', 'c':'CCONJ', 'h':'DET',
           'e':'INTJ', 'n':'NOUN', 'm':'NUM',
           'z':'PART', 'r':'PRON', 'nh':'PROPN',
           'wp':'PUNCT', 'ws':'SYM',
           'v':'VERB', 'x':'X'
          }
upos_rev_maps={'SCONJ':['c'], 'NOUN':['ni', 'nl', 'ns', 'nt', 'nz', 'n', 'nd', 'nh']}

def get_pos_mapping(pos, default_val='X'):
    if pos in upos_maps:
        return upos_maps[pos]
    else:
        for k, v in upos_rev_maps.items():
            if pos in v:
                return k
    return default_val

def nlp_procs(p, func):
    import grpc
    import nlpserv_pb2
    import nlpserv_pb2_grpc
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    # with grpc.insecure_channel('localhost:10052') as channel:
    with grpc.insecure_channel(
            target='localhost:10052',
            options=[('grpc.lb_policy_name', 'pick_first'),
                     ('grpc.enable_retries', 0), ('grpc.keepalive_timeout_ms',
                                                  10000)]) as channel:
        stub = nlpserv_pb2_grpc.NlpProcsStub(channel)
        response = func(stub, p)
    # print("Greeter client received: " + response.message)
    return response

def get_head_lemma(result, id):
    if id==0:
        return "_core_"
    for word in result.words:
        if word.id==id:
            return word.lemma

class HanlpWordImpl(WordIntf):
    def __init__(self, data):
        super().__init__(data)

    def setup(self, token):
        # print(word.id, word.lemma, word.deprel, word.head_id, \
        #  get_head_lemma(result, word.head_id))
        governor = token.head_id
        idx = token.id  # start from 1
        features = {'index': int(idx), 'text': token.lemma, 'lemma': token.name,
                    'upos': get_pos_mapping(token.postag2), 'xpos': token.postag2,
                    'feats': [token.postag1], 'governor': int(governor), 'dependency_relation': token.deprel,
                    'entity': []
                    }
        return features


class HanlpSentImpl(SentenceIntf):
    def setup(self, sent):
        words = []
        for word in sent.words:
            words.append(HanlpWordImpl(word))
        deps = []
        return words, deps

class HanlpParserImpl(object):
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, sents):
        import nlpserv_pb2
        import nlpserv_pb2_grpc

        doc = nlp_procs(sents, lambda stub, s: stub.ParseDependency(nlpserv_pb2.NlParseRequest(text=s)))
        return HanlpSentImpl(doc, text=sents)

