from sagas.runtime import runtime, DefaultImpl
from sagas.tracker_intf import TrackerIntf
from IPython.display import display

class JupyterImpl(DefaultImpl):
    def info(self, *args, sep=' ', end='\n', file=None):
        print(*args, sep=sep, end=end, file=file)

    def emphasis(self, color, *args):
        from termcolor import colored
        print(colored(' '.join(args), color))

    def dfs(self, *args):
        for arg in args:
            display(arg)

    def gv(self, dot):
        display(dot)

jupyter_inst=JupyterImpl()
def enable_jupyter_tracker():
    """
    >>> from sagas.tracker_jupyter import enable_jupyter_tracker
    >>> enable_jupyter_tracker()
    :return:
    """
    runtime.tracker=jupyter_inst

