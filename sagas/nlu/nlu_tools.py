import collections
import numpy
import sagas.tracker_fn as tc
from pprint import pprint
from sagas.conf.conf import cf

def load_corpus(dataf= "/pi/ai/seq2seq/fra-eng-2019/fra.txt"):
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
    "fr":"/pi/ai/seq2seq/fra-eng-2019/fra.txt",
    "zh":'/pi/ai/seq2seq/cmn-eng-2019/cmn.txt',
    'ja':'/pi/ai/seq2seq/jpn-eng-2019/jpn.txt',
    'de':'/pi/ai/seq2seq/deu-eng/deu.txt',
    'es':'/pi/ai/seq2seq/spa-eng/spa.txt',
    'ru':'/pi/ai/seq2seq/rus-eng/rus.txt',
    'it':'/pi/ai/seq2seq/ita-eng/ita.txt',
    'pt':'/pi/ai/seq2seq/por-eng/por.txt'
}

def to_str(obj):
    if isinstance(obj, tuple):
        return ', '.join(obj)+','
    return obj

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
            dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
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
        from sagas.nlu.google_translator import get_word_map
        from sagas.nlu.google_translator import translate
        from sagas.tool.misc import color_print

        local_trans_langs=('fa', 'ur', 'he')
        r, tracker = translate(text, source=source, target=target, options={'get_pronounce'})
        tc.info(r)
        for i, p in enumerate(tracker.pronounce):
            ps = p[2:]
            tc.info(f'v{i}="{ps}"')
        rs, trans_table=get_word_map(source, target, text,
                                     words=word_map,
                                     local_translit=True if source in local_trans_langs else False)
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

    def clip_parse(self, source, sents='', specified=None):
        """
        >> clip text: ‫یک آبجو مى خواهم.‬
        $ nlu clip_parse fa
        $ engine='stanford' nluc ar
        $ nlu clip_parse fi 'Tuolla ylhäällä asuu vanha nainen.'
        $ nluc nl 'De vrouw heeft verschillende appels.'
        $ nluc id 'Ini adalah judul buku yang saya baca.' aux

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

        list_chunks(doc_jsonify, resp, source, enable_contrast=True, specified=specified)
        words = [word.text for word in doc_jsonify.words]
        self.contrast(sents, source, word_map=words)

    def main_domains(self, sents, lang, engine=None):
        """
        $ nlu main_domains '彼のパソコンは便利じゃない。' ja knp

        :param sents:
        :param lang:
        :param engine:
        :return:
        """
        from sagas.nlu.ruleset_procs import cached_chunks, get_main_domains
        # get_main_domains('彼のパソコンは便利じゃない。', 'ja', 'knp')
        domains=get_main_domains(sents, lang, engine or cf.engine(lang))
        pprint(domains)

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

if __name__ == '__main__':
    import fire
    fire.Fire(NluTools)


