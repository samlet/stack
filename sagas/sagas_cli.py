class SagasCli(object):
    def version(self):
        from sagas.version import __version__
        print(f"sagas version: {__version__}")



