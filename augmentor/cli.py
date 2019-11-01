from pprint import pprint
import pandas as pd

class AugmentorCli(object):
    def chapters(self, lang='zh'):
        """
        $ python -m augmentor.cli chapters
        :param lang:
        :return:
        """
        dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
        del dfjson['audio']
        for name, group in dfjson.groupby('chapter'):
            print(f"`{name}`")
            del group['chapter']
            print(group)

    def chapter_titles(self, lang='zh'):
        """
        $ python -m augmentor.cli chapter_titles
        :return:
        """
        dfjson = pd.read_json(f'/pi/stack/crawlers/langcrs/all_{lang}.json')
        names= [name for name, group in dfjson.groupby('chapter')]
        pprint(names)

if __name__ == '__main__':
    import fire
    fire.Fire(AugmentorCli)

