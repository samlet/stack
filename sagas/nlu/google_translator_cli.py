from sagas.nlu.google_translator import translate
from sagas.tool import init_logger
import logging
logger = logging.getLogger(__name__)

class GoogleTranslator(object):
    def translate(self, text, target='zh-CN', source='auto', verbose=False):
        """
        $ python -m sagas.nlu.google_translator_cli translate 'Садись, где хочешь.'
        $ python -m sagas.nlu.google_translator_cli translate 'Садись, где хочешь.' en
        $ python -m sagas.nlu.google_translator_cli translate 'Садись, где хочешь.' en ru

        # multi-sentences
        $ python -m sagas.nlu.google_translator_cli translate 'Что в этом конверте? Письмо и фотографии.' ja auto True
        $ python -m sagas.nlu.google_translator_cli translate 'Что в этом конверте? Письмо и фотографии.' en auto True
        $ python -m sagas.nlu.google_translator_cli translate 'I am a student.' ar en True

        $ python -m sagas.nlu.google_translator_cli translate 'I have two refrigerators' th en True
        $ python -m sagas.nlu.google_translator_cli translate 'I have two refrigerators' iw en True
        $ python -m sagas.nlu.google_translator_cli translate '次の信号を右に曲がってください。' zh ja True

        # word translations
        $ python -m sagas.nlu.google_translator_cli translate 'city' ar en True
        $ python -m sagas.nlu.google_translator_cli translate 'tiger' lo en True
        $ python -m sagas.nlu.google_translator_cli translate 'गतिविधि' en hi True
        :param text:
        :return:
        """

        res,_ = translate(text, source=source, target=target,
                          trans_verbose=verbose,
                          # options={'disable_correct'},
                          options={'disable_correct', 'disable_cache'}
                          )
        print(res)
        # print(translate('Садись, где хочешь.'))
        # print(translate('I am a student.'))

    def trans_en(self, text, target='zh-CN'):
        """
        $ python -m sagas.nlu.google_translator_cli trans_en 'I have two refrigerators' es
        $ python -m sagas.nlu.google_translator_cli trans_en 'I have two refrigerators' he
        :param text:
        :param target:
        :return:
        """
        import sagas
        sagas.nlu.google_translator.logger.setLevel(logging.DEBUG)
        res, _ = translate(text, source='en', target=target,
                           trans_verbose=True,
                           options={'disable_correct'}
                           )
        print(res)

if __name__ == '__main__':
  import fire
  init_logger()
  fire.Fire(GoogleTranslator)

