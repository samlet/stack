import pandas as pd
from tqdm import tqdm
import requests
import os

def download_file_stream(word, url):
    # url = "http://download.thinkbroadband.com/10MB.zip"
    response = requests.get(url, stream=True)
    with open("/pi/data/audio/%s.mp3"%word, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)

def download_file(word, url, overwrites=False):
    path="/pi/data/audio/%s.mp3"%word
    if not overwrites and os.path.isfile(path):
        return False
    r = requests.get(url)
    with open(path, "wb") as handle:
        handle.write(r.content)
    return True

class RuAudio(object):
    def download_audio(self):
        """
        $ python -m sagas.ru.ru_audio download_audio
        :return:
        """
        csv_file='/Users/xiaofeiwu/tools/ai/ru/openrussian-csv/words.csv'
        df=pd.read_csv(csv_file, delimiter = '\t')
        # df[df['incomparable'].notnull()].head()
        # print(len(df))
        # df.head()
        df_as = df[df['audio'].notnull()]
        print('total audio resources', len(df_as))

        for index, row in tqdm(df.iterrows()):
            if pd.notnull(row['audio']):
                url = row['audio']
                download_file(row['bare'], url)

if __name__ == '__main__':
    import fire
    fire.Fire(RuAudio)