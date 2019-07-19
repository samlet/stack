class TermTool(object):
    def color(self):
        """
        $ python -m sagas.tests.cli.term_tool color
        :return:
        """
        from termcolor import colored
        query="That was very bad"
        topk = 5
        print('top %d questions similar to "%s"' % (topk, colored(query, 'green')))

if __name__ == '__main__':
    import fire
    fire.Fire(TermTool)

