from sagas.train.parallel_corpus import ParallelCorpus


class InteractCli(object):
    def pr(self, lang='ja', loop_for=1, host='localhost', q='.'):
        """
        $ python -m sagas.train.interact_cli pr ja
        $ python -m sagas.train.interact_cli pr ja 10 localhost
        $ python -m sagas.train.interact_cli pr ru

        # multi-lang:
            $ python -m sagas.train.interact_cli pr zh 1 pc ..
            $ python -m sagas.train.interact_cli pr fr 1 localhost ..
        :param lang:
        :param loop_for:
        :return:
        """
        pc=ParallelCorpus(host)
        pc.pr(lang, loop_for, q)

if __name__ == '__main__':
    import fire
    fire.Fire(InteractCli)
