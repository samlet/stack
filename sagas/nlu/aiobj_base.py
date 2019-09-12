from sagas.nlu.aiobj_kit import get_domains, display_result_df
from termcolor import colored

class Keeper:
    def callback(self, t):
        pass

class BaseMeta(type):
    @staticmethod
    def setup(cls):
        def _(self, lang, text, *sents):
            print(type(self).__name__,
                  isinstance(self, Keeper),
                  text, lang)
            # data = {'lang': lang, "sents": text, 'engine': 'corenlp', 'disable_predicts': False}
            # domains, meta = self.request_domains(data)
            engine = 'ltp' if lang == 'zh' else 'corenlp'
            domain_set = get_domains(text, lang, engine)
            for domains, meta in domain_set:
                # print(f"{meta['lemma']} ({meta['phonetic']}, {meta['word']})")
                # print(f"{meta['lemma']}")
                # execute rulesets
                print('rules', [r.name for r in self.rulesets])
                for i, ruleset in enumerate(self.rulesets):
                    print(colored(f"✁ {i}. {'-' * 25}", 'cyan'))
                    rule_rs = ruleset(domains, meta, self, sents)
                    display_result_df(rule_rs)

            if isinstance(self, Keeper):
                return self.callback(text)
            return None

        cls._ = lambda self, lang: lambda text, *sents: _(self, lang, text, *sents)
        cls._en = lambda self, text, *sents: _(self, 'en', text, *sents)
        cls._zh = lambda self, text, *sents: _(self, 'zh', text, *sents)
        cls._ja = lambda self, text, *sents: _(self, 'ja', text, *sents)
        cls._ko = lambda self, text, *sents: _(self, 'ko', text, *sents)



