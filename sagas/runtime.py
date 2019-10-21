from sagas.tracker_intf import TrackerIntf


class DefaultImpl(TrackerIntf):
    def info(self, *args, sep=' ', end='\n', file=None):
        print(*args, sep=sep, end=end, file=file)

    def emphasis(self, color, *args):
        from termcolor import colored
        print(colored(' '.join([str(arg) for arg in args]), color))

    def dfs(self, *args):
        import sagas
        for arg in args:
            # print(arg)
            sagas.print_df(arg)

    def gv(self, dot):
        from sagas.nlu.nlu_cli import scribes
        print(scribes(dot))

    def label_text(self, k, *args):
        from termcolor import colored
        print(colored(k, 'green'), ' '.join(args))

    def write(self, *args):
        print(*args)

class Runtime(object):
    def __init__(self):
        self.tracker = DefaultImpl()


runtime = Runtime()

