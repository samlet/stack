import logging
logger = logging.getLogger(__name__)

class NluStartup(object):
    def start(self):
        logger.info('.. start nlu comps')
        # register inspector extensions

    def shutdown(self):
        pass


