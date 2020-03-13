import logging
logger = logging.getLogger(__name__)

class NluStartup(object):
    def start(self):
        from sagas.nlu.inferencer_extensions import registry_infer_exts
        logger.info('.. start nlu comps')

        # register extensions
        registry_infer_exts()

    def shutdown(self):
        pass



