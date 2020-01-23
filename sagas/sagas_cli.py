from pprint import pprint

class SagasCli(object):
    def version(self):
        from sagas.version import __version__
        print(f"sagas version: {__version__}")

    def vis(self, sents, lang='en'):
        """
        $ sagas vis 'i am a student'
        :param sents:
        :param lang:
        :return:
        """
        from sagas.kit.analysis_kit import AnalysisKit
        AnalysisKit().console_vis(sents, lang)

    def ruleset(self, sents, intent, lang='en', graph=False):
        """
        $ sagas ruleset 'Dia datang ke Shanghai untuk menjumpai adiknya.' purpose id True
        $ sagas ruleset 'how about french food?' food en True

        :param sents:
        :param intent:
        :param lang:
        :param graph:
        :return:
        """
        from sagas.kit.rulesets_kit import RulesetsKit
        from sagas.nlu.inspector_registry import ci

        rs=RulesetsKit().execute(f"./assets/rs_common_{lang}.yml",
                              test_intent=intent,
                              test_sents=sents,
                              show_graph=graph)
        pprint(rs)

    def examples(self, intent, lang='en', graph=False):
        """
        $ sagas examples perception id

        :param intent:
        :param lang:
        :param graph:
        :return:
        """
        self.ruleset(sents=None, intent=intent, lang=lang, graph=graph)

