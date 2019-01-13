def setup_logger(log_file):
    ## add console&file loggers
    import logging

    logger = logging.getLogger()
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    # ch.setLevel(logging.ERROR)
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.setLevel(logging.INFO)

#⊕ [python - Get Output From the logging Module in IPython Notebook - Stack Overflow](https://stackoverflow.com/questions/18786912/get-output-from-the-logging-module-in-ipython-notebook)
def setup_jupyter():
    import logging
    import sys

    logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                         level=logging.INFO, stream=sys.stdout)