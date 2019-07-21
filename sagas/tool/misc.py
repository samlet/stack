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

class MiscTool(object):
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

    def trans_clip(self, source='auto', targets='zh-CN;ja', says=None, details=True):
        """
        $ trans
        $ trans auto en
        $ trans ru en
        $ trans ru 'zh-CN;ja'
        $ trans-ru
        $ trans-rus
        :return:
        """
        import clipboard
        from tqdm import tqdm
        import requests
        from sagas.nlu.google_translator import GoogleTranslator, translate

        text = clipboard.paste()
        text = text.replace("\n", "")
        target_sents=[]
        sents_map={}
        # print('❣', text)
        for target in tqdm(targets.split(';')):
            options=set()
            if says==target:
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

        if details:
            if source in ['de', 'fr', 'ru', 'es', 'it', 'pt']:
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
        clipboard.copy(result+'\n')

        if says is not None:
            from sagas.nlu.nlu_tools import NluTools
            NluTools().say(sents_map[says], says)

if __name__ == '__main__':
    import fire
    fire.Fire(MiscTool)
