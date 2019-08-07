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

# print_def=True
print_def=False
def get_verb_domains(data, return_df=False):
    import requests
    import sagas
    from sagas.nlu.rules import verb_patterns, aux_patterns, subj_patterns
    from sagas.nlu.nlu_cli import NluCli

    response = requests.post('http://localhost:8090/verb_domains', json=data)
    # print(response.status_code, response.json())
    df_set=[]
    if response.status_code == 200:
        rs = response.json()
        for r in rs:
            type_name=r['type']
            common={'lemma':r['lemma']}
            if type_name=='verb_domains':
                print('[verb]', r['lemma'], r['index'],
                      '(%s, %s)'%(r['rel'], r['governor']))
                verb_patterns({'rel':r['rel'], **common, **data}, r['domains'])
            elif type_name=='aux_domains':
                # 'rel': word.dependency_relation, 'governor': word.governor, 'head': dc.text
                delegator='☇' if not r['delegator'] else '☌'
                print('[aux]', r['lemma'], r['rel'], delegator, "%s(%s)"%(r['head'], r['head_pos']))
                # verb_patterns(r['domains'])
                aux_patterns({'pos':r['head_pos'], **common, **data}, r['domains'])
            elif type_name=='subj_domains':
                print('[subj]', r['lemma'], r['rel'], '☇', "%s(%s)"%(r['head'], ', '.join(r['head_feats'])))
                # verb_patterns(r['domains'])
                subj_patterns({'pos': r['head_pos'], **common, **data}, r['domains'])
            else:
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
    if return_df:
        return df_set

class MiscTool(object):
    # def __init__(self):
    #     self.print_def=True

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
        from tqdm import tqdm
        import requests
        from sagas.nlu.google_translator import translate
        import sagas.nlu.corenlp_helper as helper

        if sents!='':
            text=sents
            interact_mode=False
        else:
            text = clipboard.paste()
            text = text.replace("\n", "")
            interact_mode=True
        target_sents=[]
        sents_map={}
        # print('❣', text)
        if source!='auto':
            # text = fix_sents(source, text)
            sents_map[source[:2]] = text

        # addi_pronounce=[]
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
                target_sents.append(line)
                target_sents.extend(tracker.pronounce)
                sents_map[target[:2]]=trans
                # print('☌'+line)
            else:
                print('translate fail, the clipboard content has not been changed.')
                # will exit
                return
        # if len(addi_pronounce)>0:
        #     target_sents.extend(addi_pronounce)

        ## addons
        def query_serv(data, print_it=True):
            response = requests.post('http://localhost:8090/digest', json=data)
            # print(response.status_code, response.json())
            if response.status_code == 200:
                target_sents.append(response.text)

                if print_it:
                    result= response.json()
                    print_terms(data['sents'], result)
        def query_serv_zh(data, print_it=True):
            response = requests.post('http://localhost:8091/digest', json=data)
            if response.status_code == 200:
                target_sents.append(response.text)

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
                data = {'lang': 'en', "sents": sents_map['en']}
                query_serv(data)
            if 'ja' in targets:
                data = {'lang': 'ja', "sents": sents_map['ja']}
                query_serv(data)
            if 'zh' in targets:
                data = {'lang': 'zh', "sents": sents_map['zh']}
                query_serv_zh(data)

        result='\n\t'.join([text]+target_sents)
        print(result)
        if interact_mode:
            clipboard.copy(result+'\n')

        if source in available_sources:
            data = {'lang': source, "sents": text}
            get_verb_domains(data)
        elif 'en' in sents_map:
            # there is no available dep-parser for the source language,
            # use english instead of it
            data = {'lang': 'en', "sents": sents_map['en']}
            get_verb_domains(data)

        if details:
            if 'ja' in targets:
                data = {'lang': 'ja', "sents": sents_map['ja']}
                get_verb_domains(data)

        if interact_mode and says is not None:
            from sagas.nlu.nlu_tools import NluTools
            NluTools().say(sents_map[says], says)

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
