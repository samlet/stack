def get_locale(lang):
    """
    import sagas.nlu.locales as locales
    locales.get_locale('ja')
    :param lang:
    :return:
    """
    from iso639 import languages
    aragonese = languages.get(part1=lang)
    return aragonese.part3

class LocaleTable(object):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        lang, loc = key
        return self.data[(lang,loc)]

    def __setitem__(self, key, value):
        lang, loc = key
        self.data[(lang,loc)] = value

class Locales(object):
    def __init__(self):
        import json_utils
        from sagas.conf import resource_json
        # t = dd(lambda: dd(unicode))
        t=LocaleTable()
        t['eng', 'eng'] = 'English'
        t['eng', 'ind'] = 'Inggeris'
        t['eng', 'zsm'] = 'Inggeris'
        t['ind', 'eng'] = 'Indonesian'
        t['ind', 'ind'] = 'Bahasa Indonesia'
        t['ind', 'zsm'] = 'Bahasa Indonesia'
        t['zsm', 'eng'] = 'Malaysian'
        t['zsm', 'ind'] = 'Bahasa Malaysia'
        t['zsm', 'zsm'] = 'Bahasa Malaysia'
        t['msa', 'eng'] = 'Malay'

        t["swe", "eng"] = "Swedish"
        t["ell", "eng"] = "Greek"
        t["cmn", "eng"] = "Chinese (simplified)"
        t["qcn", "eng"] = "Chinese (traditional)"
        t['eng', 'cmn'] = u'英语'
        t['cmn', 'cmn'] = u'汉语'
        t['qcn', 'cmn'] = u'漢語'
        t['cmn', 'qcn'] = u'汉语'
        t['qcn', 'qcn'] = u'漢語'
        t['jpn', 'cmn'] = u'日语'
        t['jpn', 'qcn'] = u'日语'

        t['als', 'eng'] = 'Albanian'
        t['arb', 'eng'] = 'Arabic'
        t['cat', 'eng'] = 'Catalan'
        t['dan', 'eng'] = 'Danish'
        t['eus', 'eng'] = 'Basque'
        t['fas', 'eng'] = 'Farsi'
        t['fin', 'eng'] = 'Finnish'
        t['fra', 'eng'] = 'French'
        t['glg', 'eng'] = 'Galician'
        t['heb', 'eng'] = 'Hebrew'
        t['ita', 'eng'] = 'Italian'
        t['jpn', 'eng'] = 'Japanese'
        t['mkd', 'eng'] = 'Macedonian'
        t['nno', 'eng'] = 'Nynorsk'
        t['nob', 'eng'] = u'Bokmål'
        t['pol', 'eng'] = 'Polish'
        t['por', 'eng'] = 'Portuguese'
        t['slv', 'eng'] = 'Slovene'
        t['spa', 'eng'] = 'Spanish'
        t['tha', 'eng'] = 'Thai'

        self.table=t
        self.iso_map=resource_json('iso-639.json')
        self.rev_map = {v: k for k, v in self.iso_map.items()}

    def get_def(self, part3):
        from iso639 import languages
        try:
            loc = languages.get(part3=part3)
        except KeyError:
            loc = None
        return loc

    def get_code_by_part1(self, lang_part1):
        """
        $ python -m sagas.nlu.locales get_code_by_part1 en
        :param lang_part1:
        :return:
        """
        if lang_part1 in self.iso_map:
            code=self.iso_map[lang_part1]
            return code, self.get_def(code)
        return '', None

    def get_code_by_part3(self, lang_part3):
        if lang_part3 in self.rev_map:
            return self.iso_map[lang_part3], self.get_def(lang_part3)
        return '', None

    def locale(self, lang):
        """
        $ python -m sagas.nlu.locales locale 'cmn'
        :param lang:
        :return:
        """
        return self.table[lang, 'eng']

    def nltk_locales(self):
        """
        $ python -m sagas.nlu.locales nltk_locales
        :return:
        """
        from nltk.corpus import wordnet as wn
        from iso639 import languages
        import sagas
        langs = wn.langs()
        print(len(langs), sorted(langs))
        rs = []
        excepts = ['qcn']
        for lang in langs:
            if lang not in excepts:
                loc = languages.get(part3=lang)
                rs.append((loc.part3, loc.macro, loc.name))

        df=sagas.to_df(rs, ['code', 'micro', 'name'])
        sagas.print_df(df)

iso_locales=Locales()

def is_available(lang):
    return lang in iso_locales.iso_map

if __name__ == '__main__':
    import fire
    fire.Fire(Locales)

