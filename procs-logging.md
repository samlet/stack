# procs-logging.md
⊕ [Logging Cookbook — Python 3.7.2 documentation](https://docs.python.org/3/howto/logging-cookbook.html)

⊕ [python - Get Output From the logging Module in IPython Notebook - Stack Overflow](https://stackoverflow.com/questions/18786912/get-output-from-the-logging-module-in-ipython-notebook)

My understanding is that the IPython session starts up logging so basicConfig doesn't work. Here is the setup that works for me (I wish this was not so gross looking since I want to use it for almost all my notebooks):

```python
import logging
logger = logging.getLogger()
fhandler = logging.FileHandler(filename='mylog.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)

## add console&file loggers
import logging

logger = logging.getLogger()
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.setLevel(logging.INFO)
```

Now when I run:

```python
logging.error('hello!')
logging.debug('This is a debug message')
logging.info('this is an info message')
logging.warning('tbllalfhldfhd, warning.')
```

I get a "mylog.log" file in the same directory as my notebook that contains:

2015-01-28 09:49:25,026 - root - ERROR - hello!
2015-01-28 09:49:25,028 - root - DEBUG - This is a debug message
2015-01-28 09:49:25,029 - root - INFO - this is an info message
2015-01-28 09:49:25,032 - root - WARNING - tbllalfhldfhd, warning.
Note that if you rerun this without restarting the IPython session it will write duplicate entries to the file since there would now be two file handlers defined


