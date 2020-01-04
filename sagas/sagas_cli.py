class SagasCli(object):
    def version(self):
        from sagas.version import __version__
        print(f"sagas version: {__version__}")

    def vis(self, sents, lang='en'):
        from sagas.kit.analysis_kit import AnalysisKit
        AnalysisKit().console_vis(sents, lang)
