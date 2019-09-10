from unittest import TestCase


class TestGet_domains(TestCase):
    def test_get_domains(self):
        from sagas.nlu.aiobj_kit import get_domains
        get_domains('你有几台笔记本电脑？', 'zh', 'ltp')
        print('done.')
        # self.fail()

    def test_get_domains_2(self):
        from sagas.nlu.aiobj_kit import get_domains
        get_domains('我要点一个炸鸡。', 'zh', 'ltp')
        print('done.')
        # self.fail()
