# procs-logging.md
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


