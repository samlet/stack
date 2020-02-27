import time
# from sagas.nlu.nlu_tools import NluTools
from sagas.nlu.google_translator import translate

class KoreaProcessor(object):
    def __init__(self):
        import pyttsx3
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')  # getting details of current voice
        langs = [v.languages[0] for v in voices]
        ids = [v.id for v in voices]
        self.langs_map = dict(zip(langs, ids))

    def say_in(self, sents, lang, rate=200):
        self.engine.setProperty('rate', rate)  # setting up new voice rate
        self.engine.setProperty('voice', self.langs_map[lang])
        self.engine.say(sents)
        self.engine.runAndWait()

    def process(self, source, target, text, ips_idx=1):
        """
        from sagas.ko.korea_processor import KoreaProcessor
        kp=KoreaProcessor()
        kp.process('ko', 'en', '나는 냉장고가 두 개있다.', 0)

        see also: procs-ko-tr.ipynb
        :param source:
        :param target:
        :param text:
        :param ips_idx:
        :return:
        """
        verbose = False
        options = {'get_pronounce'}
        # options.add('get_pronounce')
        res, t = translate(text, source=source, target=target,
                           trans_verbose=verbose, options=options)
        # print(res, text, t[ips_idx])
        print('✁', '%s(%s %s)' % (text, res, t.pronounce[ips_idx]))
        for sent in text.split(' '):
            res, t = translate(sent, source=source, target=target,
                               trans_verbose=verbose, options=options)
            # print(res, sent, t[ips_idx])
            print('%s(%s,%s)' % (sent, res, t.pronounce[ips_idx][1:]), end=" ")
            time.sleep(0.05)
        print('.')

    def analyse_ko(self, text):
        """
        $ python -m sagas.ko.korea_processor analyse_ko '그렇게 큰 규모는 아니었습니다.'
        :param text:
        :return:
        """
        target = 'zh-CN'
        self.process('ko', target, text)
        # NluTools().say(text, 'ko')
        self.say_in(text, 'ko_KR', 200)

    def analyse(self, sents_zh):
        """
        analyse('现在整个世界都变成了一个村庄。')
        $ python -m sagas.ko.korea_processor analyse '现在整个世界都变成了一个村庄。'
        $ ko 美丽的花开得很好。
        $ ko 姐姐买来了新衣服。
        :param sents_zh:
        :return:
        """
        # translate from chinese to korea
        sents_ko, _ = translate(sents_zh, source='zh-CN', target='ko')
        print('✔', sents_ko)
        self.process('ko', 'zh-CN', sents_ko)
        # NluTools().say(sents_ko, 'ko')
        self.say_in(sents_ko, 'ko_KR', 200)

if __name__ == '__main__':
    import fire
    fire.Fire(KoreaProcessor)

