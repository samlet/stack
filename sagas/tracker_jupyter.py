from sagas.nlu.env import sa_env
from sagas.runtime import runtime, DefaultImpl
from sagas.tracker_intf import TrackerIntf
from IPython.display import display

class JupyterImpl(DefaultImpl):
    def dfs(self, *args):
        for arg in args:
            display(arg)

    def gv(self, dot):
        display(dot)

    def write(self, *args):
        display(*args)

jupyter_inst=JupyterImpl()
def enable_jupyter_tracker():
    """
    >>> from sagas.tracker_jupyter import enable_jupyter_tracker
    >>> enable_jupyter_tracker()
    :return:
    """
    sa_env.runtime = 'streamlit'
    runtime.tracker=jupyter_inst

