import logging
import logging.config
import yaml

# ⊕ [Logging in Python – Real Python](https://realpython.com/python-logging/)
with open('../../conf/logger.yml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)

logger.debug('This is a debug message')
msg='hi'
logger.info(f"{msg}")

