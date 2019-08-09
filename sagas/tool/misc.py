from time import sleep

def print_terms(sents, result):
    from termcolor import colored
    for verb in result['verbs']:
        sents = sents.replace(verb[0], colored(verb[0], 'green'))
    for item, value in result.items():
        if 'subj' in item:
            sents = sents.replace(value, colored(value, 'red'))
        if 'obj' in item:
            sents = sents.replace(value, colored(value, 'blue'))
        if 'cop' in item:
            sents = sents.replace(value, colored(value, 'magenta'))
        if 'obl' in item:
            sents = sents.replace(value, colored(value, 'yellow'))
    print('%s: %s' % (result['lang'], sents))

def print_terms_zh(sents, result):
    from termcolor import colored
    for verb in result['verbs']:
        sents = sents.replace(verb, colored(verb, 'green'))
    for item, value in result.items():
        if 'sbv' in item:
            sents = sents.replace(value, colored(value, 'red'))
        if 'ob' in item:
            sents = sents.replace(value, colored(value, 'blue'))
        # if 'cop' in item:
        #     sents = sents.replace(value, colored(value, 'magenta'))
    print('%s: %s' % (result['lang'], sents))

# stem_filters=['obj', 'nsubj']
def print_stem_chunks(r):
    from termcolor import colored
    for stem in r['stems']:
        # if stem[0] in stem_filters:
        if len(stem[1])>1:
            value=' '.join(stem[1])
            print('%s ->'%stem[0], colored(value, 'green'))

display_synsets_opts=['nsubj', 'obl', 'obj', 'iobj']
def display_synsets(meta, r, lang):
    from sagas.nlu.nlu_cli import retrieve_word_info
    from termcolor import colored

    from sagas.nlu.inspector_common import Context
    ctx=Context(meta, r['domains'])

    resp=[]
    word = r['lemma']
    def retrieve(word, indicator):
        rs = retrieve_word_info('get_synsets', word, lang, '*')
        if len(rs) > 0:
            print('♥ %s(%s): %s' % (colored(word, 'magenta'), indicator, ', '.join(rs)))
            resp.append('♥ %s(%s): %s' % (word, indicator, ', '.join(rs)))
    retrieve(word, '~')
    for opt in display_synsets_opts:
        if opt in ctx.lemmas:
            retrieve(ctx.lemmas[opt], opt)
    return resp

# print_def=True
print_def=False
print_synsets=True
def get_verb_domains(data, return_df=False):
    import requests
    import sagas
    from sagas.nlu.rules import verb_patterns, aux_patterns, subj_patterns
    from sagas.nlu.nlu_cli import NluCli

    response = requests.post('http://localhost:8090/verb_domains', json=data)
    # print(response.status_code, response.json())
    df_set=[]
    result=[]
    if response.status_code == 200:
        rs = response.json()
        for r in rs:
            type_name=r['type']
            common={'lemma':r['lemma']}
            if type_name=='verb_domains':
                print('[verb]', r['lemma'], r['index'],
                      '(%s, %s)'%(r['rel'], r['governor']))
                meta={'rel':r['rel'], **common, **data}
                verb_patterns(meta, r['domains'])
            elif type_name=='aux_domains':
                # 'rel': word.dependency_relation, 'governor': word.governor, 'head': dc.text
                delegator='☇' if not r['delegator'] else '☌'
                print('[aux]', r['lemma'], r['rel'], delegator, "%s(%s)"%(r['head'], r['head_pos']))
                # verb_patterns(r['domains'])
                meta={'pos':r['head_pos'], **common, **data}
                aux_patterns(meta, r['domains'])
            elif type_name=='subj_domains':
                print('[subj]', r['lemma'], r['rel'], '☇', "%s(%s)"%(r['head'], ', '.join(r['head_feats'])))
                # verb_patterns(r['domains'])
                meta={'pos': r['head_pos'], **common, **data}
                subj_patterns(meta, r['domains'])
            else:
                meta = {}
                raise Exception('Cannot process specific type: {}'.format(type_name))

            # df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'children', 'features'])
            df = sagas.to_df(r['domains'], ['rel', 'index', 'text', 'lemma', 'children', 'features'])
            df_set.append(df)
            if not return_df:
                # where 1 is the axis number (0 for rows and 1 for columns.)
                df = df.drop('children', 1)
                sagas.print_df(df)
                print_stem_chunks(r)

                if print_def:
                    NluCli().get_word_def(r['lemma'], data['lang'])
                if print_synsets:
                    r=display_synsets(meta, r, data['lang'])
                    result.extend(r)


    if return_df:
        return df_set
    else:
        # print(result)
        return result

class TransContext(object):
    def __init__(self, s,t,q,says):
        self.target_sents = []
        self.sents_map = {}

        self.source=s
        self.targets=t
        self.text=q
        self.says=says

    def pars(self):
        return self.source, self.targets, self.text, self.says

class MiscTool(object):
    def __init__(self):
        import sagas.conf.conf as conf
        cf = conf.TransClipConf()
        self.translator=cf.conf['translator']
        print('.. using translator', self.translator)
        self.translators={'baidu':self.trans_baidu,
                          'google':self.trans_google}

    def plain(self):
        """
        $ python -m sagas.tool.misc plain
        :return:
        """
        import clipboard
        text = clipboard.paste()
        text = text.replace("\n", "")
        # print(text)
        clipboard.copy(text)
        return text

    def add_serial_no(self):
        """
        $ python -m sagas.tool.misc add_serial_no
        :return:
        """
        import clipboard
        text = clipboard.paste()
        begin = 1
        result = []
        for line in text.splitlines():
            result.append(str(begin) + ". " + line)
            begin = begin + 1
        clipboard.copy("\n".join(result))

    def wrap_sent(self):
        """
        $ python -m sagas.tool.misc wrap_sent
        :return:
        """
        import clipboard
        text = clipboard.paste()
        text = "'%s', "%(text.replace("\n", ""))
        clipboard.copy(text)
        return text

    def trans_google(self, ctx:TransContext):
        from tqdm import tqdm
        from sagas.nlu.google_translator import translate
        import time
        import random
        source, targets, text, says=ctx.pars()

        for target in tqdm(targets.split(';')):
            options=set()
            # default options
            options.add('disable_correct')
            if says==target:
                options.add('get_pronounce')
            if says==source and target=='en':
                options.add('get_pronounce')

            trans, tracker=translate(text, source=source, target=target, options=options)
            if trans=='':
                print('wait a second, try again ...')
                sleep(1)
                trans, tracker = translate(text, source=source, target=target, options=options)

            if trans != '':
                # result=text+'\n\t* '+trans+'\n'
                line='[%s] '%target[:2]+trans
                ctx.target_sents.append(line)
                ctx.target_sents.extend(tracker.pronounce)
                ctx.sents_map[target[:2]]=trans
                # print('☌'+line)
            else:
                print('translate fail, the clipboard content has not been changed.')
                # will exit
                return False

            time.sleep(random.uniform(0.05, 0.20))

        return True

    def trans_baidu(self, ctx: TransContext):
        from tqdm import tqdm
        from sagas.nlu.baidu_translator import BaiduTranslator
        import time

        tr=BaiduTranslator()
        for t in tqdm(ctx.targets.split(';')):
            result=tr.trans(ctx.source, t, ctx.text)
            # print(result)
            trans=result[0]['dst']
            line = '[%s] ' % t[:2] + trans
            ctx.target_sents.append(line)
            ctx.sents_map[t[:2]] = trans

            time.sleep(1.0)  # must wait 1 second
        return True

    def trans_clip(self, source='auto', targets='zh-CN;ja', says=None, details=True, sents=''):
        """
        $ trans
        $ trans auto en
        $ trans ru en
        $ trans ru 'zh-CN;ja'
        $ trans-ru
        $ trans-rus

        $ alias sp="python -m sagas.tool.misc trans_clip pt 'en;it;ja' ja False"
        $ sp 'O homem fica amarelo.'
        :return:
        """
        import clipboard
        import requests
        import sagas.nlu.corenlp_helper as helper

        if sents!='':
            text=sents
            interact_mode=False
        else:
            text = clipboard.paste()
            text = text.replace("\n", "")
            interact_mode=True
        # target_sents=[]
        # sents_map={}
        ctx=TransContext(source, targets, text, says)
        # print('❣', text)
        if source!='auto':
            # text = fix_sents(source, text)
            ctx.sents_map[source[:2]] = text

        # addi_pronounce=[]
        # succ=self.trans_google(ctx)
        succ=self.translators[self.translator](ctx)

        if not succ:
            return
        # if len(addi_pronounce)>0:
        #     target_sents.extend(addi_pronounce)

        ## addons
        def query_serv(data, print_it=True):
            response = requests.post('http://localhost:8090/digest', json=data)
            # print(response.status_code, response.json())
            if response.status_code == 200:
                ctx.target_sents.append(response.text)

                if print_it:
                    result= response.json()
                    print_terms(data['sents'], result)
        def query_serv_zh(data, print_it=True):
            response = requests.post('http://localhost:8091/digest', json=data)
            if response.status_code == 200:
                ctx.target_sents.append(response.text)

                if print_it:
                    result= response.json()
                    print_terms_zh(data['sents'], result)

        # available_sources=['en', 'de', 'fr', 'ru', 'es', 'it', 'pt', 'cs', 'sk', 'pl', 'tr',
        #                    'sv', 'no', 'hi']
        available_sources=helper.langs.keys()
        if details:
            if source in available_sources:
                data = {'lang': source, "sents": text}
                query_serv(data)

            # common targets
            if 'en' in targets:
                data = {'lang': 'en', "sents": ctx.sents_map['en']}
                query_serv(data)
            if 'ja' in targets:
                data = {'lang': 'ja', "sents": ctx.sents_map['ja']}
                query_serv(data)
            if 'zh' in targets:
                data = {'lang': 'zh', "sents": ctx.sents_map['zh']}
                query_serv_zh(data)

        result='\n\t'.join([text]+ctx.target_sents)
        print(result)

        addons=[]
        if source in available_sources:
            data = {'lang': source, "sents": text}
            addons.extend(get_verb_domains(data))
        elif 'en' in ctx.sents_map:
            # there is no available dep-parser for the source language,
            # use english instead of it
            data = {'lang': 'en', "sents": ctx.sents_map['en']}
            addons.extend(get_verb_domains(data))

        if details:
            if 'ja' in targets:
                data = {'lang': 'ja', "sents": ctx.sents_map['ja']}
                get_verb_domains(data)

        if interact_mode:
            if len(addons)>0:
                result=result+'\n\t'+'\n\t'.join(addons)
            clipboard.copy(result+'\n')

        if interact_mode and says is not None:
            from sagas.nlu.nlu_tools import NluTools
            NluTools().say(ctx.sents_map[says], says)

    def verb_domains(self, sents, lang='en'):
        """
        $ python -m sagas.tool.misc verb_domains 'Мы написали три книги за год.' ru
        :param sents:
        :param lang:
        :return:
        """
        data = {'lang': lang, "sents": sents}
        get_verb_domains(data)

if __name__ == '__main__':
    import fire
    fire.Fire(MiscTool)
