import logging
logger = logging.getLogger(__name__)

class NluStartup(object):
    def start(self):
        from sagas.nlu.inferencer_extensions import registry_infer_exts
        from sagas.nlu.signals import signals
        from . import processors

        logger.info('.. start nlu comps')

        # register extensions
        registry_infer_exts()
        signals.registry_signals(processors.evts)

    def shutdown(self):
        pass



