import logging.config
import yaml

def init_logger():
    from sagas.conf import resource_path
    file=resource_path('logger.yml')
    with open(file, 'r') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)

# Usage:
# logger = logging.getLogger(__name__)
#
# logger.debug('This is a debug message')
# msg='hi'
# logger.info(f"{msg}")

