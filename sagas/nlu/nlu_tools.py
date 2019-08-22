import collections

from sagas.nlu.corpus_helper import filter_term, lines, divide_chunks
import numpy
import spacy

def load_corpus(dataf= "/pi/ai/seq2seq/fra-eng-2019/fra.txt"):
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

    def parse_sentence(self, lang, sents):
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
        response = requests.post(f'{cf.common_s}/digest', json=data)
        # print(response.status_code, response.json())
        if response.status_code == 200:
            print(response.text)
            clipboard.copy(response.text)

if __name__ == '__main__':
    import fire
    fire.Fire(NluTools)
