class CommonTests(object):
    def progress(self):
        """
        $ python -m sagas.tests.test_common progress
        :return:
        """
        from tqdm import tqdm, trange
        import time

        text = ""
        for char in tqdm(["a", "b", "c", "d"]):
            time.sleep(0.25)
            text = text + char

        for i in trange(100):
            time.sleep(0.01)

if __name__ == '__main__':
    import fire
    fire.Fire(CommonTests)

