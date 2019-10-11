import stanfordnlp.server as corenlp

lang_mappings={'ar':'arabic', 'en':'english'}
class StanfordHelper(object):
    def __init__(self, host='localhost', port=9005):
        self.host=host
        self.port=port
        self.external_server_client = corenlp.CoreNLPClient(start_server=False,
                                                       endpoint=f"http://{self.host}:{self.port}")

    def invoke_server(self, text, language, output_format='json'):
        # output_format='json'  # output type from server: serialized, json, text, conll, conllu, or xml
        ann = self.external_server_client.annotate(text, annotators='tokenize,ssplit,pos,depparse,lemma,natlog,ner,openie',
                                              properties_key=language,
                                              output_format=output_format)
        return ann

    def parse(self, text, lang):
        return self.invoke_server(text, language=lang_mappings[lang])

    def parse_df(self, sents, lang='ar'):
        import sagas
        result_dfs = {}
        ann = self.invoke_server(sents, language=lang_mappings[lang])
        tokens = ann['sentences'][0]['tokens']
        result_dfs['tokens']=sagas.dict_df(tokens)
        result_dfs['deps']=sagas.dict_df(ann['sentences'][0]['enhancedPlusPlusDependencies'])
        openie = ann['sentences'][0]['openie']
        result_dfs['openie']=sagas.dict_df(openie)
        return ann, result_dfs

    def parse_print(self, sents, format='default'):
        """
        $ python -m sagas.nlu.stanford_helper parse_print 'جارك رجل طيب'
        :param sents:
        :param format:
        :return:
        """

        import json
        import sagas

        # TEXT = 'جارك رجل طيب'
        # host = 'pc'
        ann=self.invoke_server(sents, 'arabic', output_format='text' if format=='default' else 'json')
        if format=='default':
            print(ann.strip())
        elif format=='json':
            print(', '.join(ann['sentences'][0].keys()))
            print(json.dumps(ann, indent=2, ensure_ascii=False))
        elif format=='df':
            tokens = ann['sentences'][0]['tokens']
            sagas.print_df(sagas.dict_df(tokens))

    def show_deps(self, sents, lang='ar'):
        language=lang_mappings[lang]
        ann = self.invoke_server(sents, language, 'json')
        display_result(ann)
        viz = BasicViz()
        tokens = ann['sentences'][0]['tokens']
        nodes = {t['index']: {'word': t['word'],
                              'style': 'dashed' if t['pos'].startswith('V') else 'solid',
                              'color': 'black' if t['ner'] == 'O' else 'blue',
                              } for t in tokens}
        nodes[0] = {'word': 'ROOT', 'style': 'filled', 'color': 'lightgrey'}
        viz.add_nodes(nodes)
        deps = ann['sentences'][0]['enhancedPlusPlusDependencies']
        viz.add_edges([(t['dependentGloss'], t['governorGloss'], t['dep']) for t in deps])
        return viz.f

def display_result(ann):
    import sagas
    from IPython.display import display
    tokens=ann['sentences'][0]['tokens']
    display(sagas.dict_df(tokens))
    display(sagas.dict_df(ann['sentences'][0]['enhancedPlusPlusDependencies']))

def inspect_text(sents, lang='en', host='localhost', port=9001):
    # 'Joe Smith lives in California.'
    serv=StanfordHelper(host=host, port=port)
    r = serv.invoke_server(sents, lang_mappings[lang], 'json')
    display_result(r)


class BasicViz(object):
    def __init__(self, shape='egg', size='8,5', fontsize=0):
        from graphviz import Digraph
        self.f = Digraph('deps', filename='deps.gv')
        self.f.attr(rankdir='LR', size=size)
        # font 'Calibri' support Arabic text
        self.f.attr('node', shape=shape, fontname='Calibri')
        if fontsize != 0:
            self.f.attr(fontsize=str(fontsize))

    def default_node(self):
        self.f.attr('node', style='solid', color='black')

    def add_nodes(self, nodes):
        for k, v in nodes.items():
            self.f.attr('node', style=v['style'], color=v['color'])
            self.f.node(v['word'])
            self.default_node()

    def add_edges(self, edges):
        for edge in edges:
            # print(edge)
            head_node = edge[1]
            rel = edge[2]
            node = edge[0]
            self.f.edge(head_node, node, label=rel, fontsize='11', fontname='Calibri')
        return self.f


sf_confs={'en':('localhost', 9001),
          'ar':('localhost', 9005),
          }
sf_services={}
def get_sf_service(lang):
    if lang not in sf_services:
        conf=sf_confs[lang]
        sf_services[lang]=StanfordHelper(host=conf[0], port=conf[1])
    return sf_services[lang]

if __name__ == '__main__':
    import fire
    fire.Fire(StanfordHelper)

