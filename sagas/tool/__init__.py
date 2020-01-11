from .loggers import init_logger
import sagas.tracker_fn as tc

def color_print(color:str, text):
    # from termcolor import colored
    if isinstance(text, list):
        for t in text:
            tc.emp(color, t)
    else:
        tc.emp(color, text)

