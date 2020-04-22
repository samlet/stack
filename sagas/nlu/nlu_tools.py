from typing import Text, Any, Dict, List, Union

import collections
import numpy
import sagas.tracker_fn as tc
from pprint import pprint
from sagas.conf.conf import cf
from sagas.nlu.constants import contrast_translit_langs
from sagas.startup import startup


def load_corpus(dataf= f"{cf.conf_dir}/ai/seq2seq/fra-eng-2019/fra.txt"):
    from sagas.nlu.corpus_helper import filter_term, lines, divide_chunks
    # print('loading spacy english model ...')
    # nlp_spacy = spacy.load('en_core_web_sm')
    print('loading corpus ...')
    pairs = lines(dataf)
    total = len(pairs)
    print('total', total)
    array = numpy.array(pairs)
    random_rows = numpy.random.randint(total, size=10)
    print('pickup', random_rows)
    print(array[random_rows, :])

    # print('analyse ...')
    rows = array[random_rows, :]
    dataset = []
    # for r in rows:
    #     sents=str(r[0])
    #     tr_lang=str(r[1].strip())
    return rows

corpus_resources={
    "fr":f"{cf.conf_dir}/ai/seq2seq/fra-eng-2019/fra.txt",
    "zh":f'{cf.conf_dir}/ai/seq2seq/cmn-eng-2019/cmn.txt',
    'ja':f'{cf.conf_dir}/ai/seq2seq/jpn-eng-2019/jpn.txt',
    'de':f'{cf.conf_dir}/ai/seq2seq/deu-eng/deu.txt',
    'es':f'{cf.conf_dir}/ai/seq2seq/spa-eng/spa.txt',
    'ru':f'{cf.conf_dir}/ai/seq2seq/rus-eng/rus.txt',
    'it':f'{cf.conf_dir}/ai/seq2seq/ita-eng/ita.txt',
    'pt':f'{cf.conf_dir}/ai/seq2seq/por-eng/por.txt'
}

def to_str(obj):
    if isinstance(obj, tuple):
        return ', '.join(obj)+','
    return obj

def treeing(ds):
    """ 将解析树转化为anytree形式, 以便遍历或可视化 """
    child_tags=[k for k,v in ds.items() if isinstance(v, list) and k not in ('entity', 'segments')]
    data={'children':[]}
    for k,v in ds.items():
        if k in child_tags:
            for vchild in v:
                data['children'].append(treeing(vchild))
        else:
            data[k]=v
    return data

def vis_tree(ds:Dict[Text, Any], lang, trans=False):
    """ 可视化domains """
    from anytree.importer import DictImporter
    from anytree import RenderTree
    from sagas.nlu.translator import get_contrast

    data = treeing(ds)
    importer = DictImporter()
    tree_root = importer.import_(data)
    tree = RenderTree(tree_root)
    for pre, fill, node in tree:
        if node.dependency_relation=='punct':
            addons='_'
        else:
            addons=f"{node.lemma}; {get_contrast(node.text, lang)}" \
                if trans else f"{node.lemma}"
        print(f"{pre}{node.dependency_relation}: "
              f"{node.text}({addons}, {node.upos.lower()}, {node.index})")

class NluTools(object):
    def say(self, text, lang='en'):
        """
        $ python -m sagas.nlu.nlu_tools say 'hello' en
        $ python -m sagas.nlu.nlu_tools say 'Они спрашивают, где коробка.' ru
        :param text:
        :param lang:
        :return:
        """
        from sagas.nlu.tts_utils import say_lang
        say_lang(text, lang)

    def say_with(self, lang, *items):
        """
        $ python -m sagas.nlu.nlu_tools say_with ru Они спрашивают, где коробка.
        $ python -m sagas.nlu.nlu_tools say_with ar 'أنا طالب'
        $ say-ru Они спрашивают, где коробка.
        :param lang:
        :param items:
        :return:
        """
        sents = ' '.join([to_str(item) for item in items])
        print(sents)
        self.say(sents, lang)

    def practice(self, lang_tr='fr', use_latest=False):
        """
        $ python -m sagas.nlu.nlu_tools practice fr
        :param lang:
        :param lang_tr:
        :param dataf:
        :return:
        """
        from sagas.nlu.tts_utils import say_lang
        import json_utils

        lang = 'en'
        dataf=corpus_resources[lang_tr]
        rows=[]
        if use_latest:
            rows = json_utils.read_json_file('./out/latest_%s.json' % lang_tr)
        else:
            rows=load_corpus(dataf)
            json_utils.write_json_to_file('./out/latest_%s.json' % lang_tr, rows.tolist())
        for r in rows:
            sents = str(r[0])
            tr_lang = str(r[1].strip())
            say_lang(sents, lang)
            print('♥', sents)
            say_lang(tr_lang, lang_tr)
            print('♡', tr_lang)

    def all_voices(self, lang=None):
        """
        $ python -m sagas.nlu.nlu_tools all_voices
        $ nlu all-voices ru
        :return:
        """
        import pyttsx3
        import sagas
        engine = pyttsx3.init()
        voices: collections.Iterable = engine.getProperty('voices')
        rs=[]
        for voice in voices:
            if lang is not None:
                if voice.languages[0].startswith(lang):
                    print(voice)
            else:
                print(voice, voice.id, voice.languages[0])
                rs.append((voice.id.replace('com.apple.speech.synthesis.',''),
                           voice.name,
                           voice.languages,
                           voice.gender
                           ))
        rs=sorted(rs, key=lambda el: el[2][0])
        sagas.print_df(sagas.to_df(rs, ['id', 'name', 'lang', 'gender']))

    def chapters(self, lang='ja'):
        """
        $ nlu chapters ru

        :param lang:
        :return:
        """
        import pandas as pd
        from pprint import pprint
        def list_chapter_titles(lang):
            dfjson = pd.read_json(f'{cf.conf_dir}/stack/crawlers/langcrs/all_{lang}.json')
            return [name for name, group in dfjson.groupby('chapter')]

        rs=list_chapter_titles(lang)
        pprint(rs)

    def parse_sentence(self, lang, sents, engine='corenlp'):
        """
        $ python -m sagas.nlu.nlu_tools parse_sentence ja '今調査します'
        :param lang:
        :param sents:
        :return:
        """
        import requests
        import clipboard
        from sagas.conf.conf import cf
        data = {'lang': lang, "sents": sents}
        response = requests.post(f'{cf.servant(engine)}/digest', json=data)
        # print(response.status_code, response.json())
        if response.status_code == 200:
            print(response.text)
            clipboard.copy(response.text)

    def contrast(self, text, source, target='en', word_map=None):
        """
        $ nlu contrast '저는 허락을 못 받아서 안 왔어요.' ko
        :param text:
        :param source:
        :param target:
        :return:
        """
        from sagas.nlu.translator import get_word_map
        from sagas.nlu.translator import translate
        from sagas.tool.misc import color_print

        r, tracker = translate(text, source=source, target=target, options={'get_pronounce'})
        tc.info(r)
        for i, p in enumerate(tracker.pronounce):
            ps = p[2:]
            tc.info(f'v{i}="{ps}"')
        rs, trans_table=get_word_map(source, target, text,
                                     words=word_map,
                                     local_translit=True if source in contrast_translit_langs else False)
        for i, (k, r) in enumerate(rs.items()):
            tc.info(f"{i} - ", r.replace('\n', ' '))

        color_print('cyan', ' '.join(trans_table))

    def clip_contrast(self, source):
        """
        $ nlu clip_contrast fa
        :param source:
        :return:
        """
        from sagas.nlu.common import get_from_clip
        text=get_from_clip()
        if text.strip()=='':
            print('no text avaliable in clipboard.')
            return
        print(text)
        self.contrast(text, source)

    def clip_parse(self, source, sents='', specified='default', do_test=False):
        """
        >> clip text: ‫یک آبجو مى خواهم.‬
        $ nlu clip_parse fa
        $ engine='stanford' nluc ar
        $ nlu clip_parse fi 'Tuolla ylhäällä asuu vanha nainen.'
        $ nluc nl 'De vrouw heeft verschillende appels.'
        $ nluc id 'Ini adalah judul buku yang saya baca.' aux
        $ nluc fi 'Voiko täältä lainata aurinkovarjoa?' default True

        :param source:
        :return:
        """
        from sagas.nlu.uni_remote import dep_parse
        from sagas.nlu.common import get_from_clip
        from sagas.conf.conf import cf
        from sagas.nlu.uni_remote_viz import list_chunks
        from sagas.nlu.utils import fix_sents

        if sents=='':
            sents = get_from_clip()
            if sents.strip()=='':
                tc.info('no text avaliable in clipboard.')
                return
        sents=fix_sents(sents, source)
        tc.info(sents)

        # Parse the sentence and display it's chunks, domains and contrast translations.
        engine=cf.engine(source)
        doc_jsonify, resp = dep_parse(sents, source, engine, ['predicts'])
        if doc_jsonify is None:
            raise Exception(f'Cannot parse sentence for lang {source}')

        list_chunks(doc_jsonify, resp, source,
                    enable_contrast=True,
                    specified=None if specified=='default' else specified)
        words = [word.text for word in doc_jsonify.words]
        self.contrast(sents, source, word_map=words)

        ## visual tree
        self.main_domains(sents, source, engine, False)
        ## add rulesets procs
        from sagas.nlu.inferencer import do_infers
        cli_cmd, pats = do_infers(sents, source)
        if do_test:
            for pat in pats:
                self.check_rule(sents, source, pat)

    def main_domains(self, sents, lang, engine=None, print_domains=True):
        """
        $ nlu main_domains '彼のパソコンは便利じゃない。' ja knp
        $ nlu main_domains 'これを作ってあげました。' ja
        $ nlu main_domains 'What do you think about the war?' en
        $ engine='stanza' nluc en 'I was born in Beijing.'

        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.ruleset_procs import cached_chunks, get_main_domains
        # get_main_domains('彼のパソコンは便利じゃない。', 'ja', 'knp')
        engine=engine or cf.engine(lang)
        domain, domains = get_main_domains(sents, lang, engine)
        if print_domains:
            print('domain type:', domain)
            pprint(domains)

        if domain != 'predicts':
            tc.emp('cyan', f"✁ tree vis {domain}, {engine} {'-' * 25}")
            for ds in domains:
                    vis_tree(ds, lang)

    def doc(self, sents, lang, engine=None):
        """
        $ nlu doc 'これを作ってあげました。' ja analspa
        $ nlu doc '主FAX番号はありますか' ja analspa
        $ nlu doc '你在北京的公司的主要传真号码是什么' zh analz
        $ nlu doc '你在北京的公司的主要传真号码是什么' zh analspa
        $ nlu doc "Alex Smith was working at Acme Corp Inc." en spacy
        $ nlu doc 'this is a digital good' en

        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.ruleset_procs import parse_sents
        data = {'lang': lang, "sents": sents, 'engine': engine or cf.engine(lang)}
        doc_jsonify, resp = parse_sents(data)
        pprint(doc_jsonify.as_json)

    def tree_comp(self, sents, lang):
        """
        $ nlu tree_comp 'What do you think about the war?' en
        $ nlu tree_comp 'A casa tem dezenove quartos.' pt
        $ nlu tree_comp "Por que você não perguntou?" pt
        $ nlu tree_comp "I postini lavorano di mattina." it

        :param sents:
        :param lang:
        :return:
        """
        from sagas.nlu.ruleset_procs import cached_chunks, get_main_domains
        from sagas.nlu.spacy_helper import is_available

        if not sents or sents=='_':
            import clipboard
            text = clipboard.paste()
            sents = text.replace("\n", "")

        print(f'$ nlu tree_comp "{sents}" {lang}')
        engines=['corenlp', 'stanza']
        if is_available(lang):
            engines.append('spacy_2.2')
        tags_map={}
        for engine in engines:
            domain, domains = get_main_domains(sents, lang, engine)
            if domain != 'predicts':
                tc.emp('cyan', f"✁ tree vis {domain}, {engine} {'-' * 25}")
                for ds in domains:
                    vis_tree(ds, lang)
            tags_map[engine] = [k for k, v in domains[0].items() if isinstance(v, list) and k not in ('entity', 'segments')]

        diff=set(tags_map['corenlp']).symmetric_difference(set(tags_map['stanza']))
        if diff:
            tc.emp('red', 'differences', diff)
        else:
            tc.emp('green', 'no differences')

    def check_rule(self, sents, lang, rule, engine=None):
        """
        $ nlu check_rule '彼のパソコンは便利じゃない。' ja \
            "subj('adj',ガ=kindof('artifact', 'n'))"

        :param sents:
        :param lang:
        :param rule:
        :return:
        """
        from sagas.tool.dynamic_rules import DynamicRules
        data = {'lang': lang, "sents": sents}
        DynamicRules().predict(data, rule, engine=engine or cf.engine(lang))

    def infer(self, sents, lang='en', verbose=False):
        """
        $ python -m sagas.nlu.nlu_tools infer '水としょうゆを混ぜた。' ja
            pat(5, name='predict_mix').verb(specsof('*', 'mix'), ヲ=kindof('water', '*')),
        $ python -m sagas.nlu.nlu_tools infer 'Ellos ya leyeron ese libro en la escuela.' es
            pat(5, name='behave_read').verb(extract_for('plain', 'advmod'), behaveof('read', 'v'), nsubj=agency, obl=kindof('school', '*'), obj=kindof('book', '*')),

        :param sents:
        :param lang:
        :return:
        """
        from sagas.nlu.inferencer import Inferencer
        infers = Inferencer(lang)
        return infers.infer(sents, verbose=verbose)

if __name__ == '__main__':

    import fire


    startup.start()
    fire.Fire(NluTools)


