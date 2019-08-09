import os

appid = os.environ.get('baidu_appid')  # 你的appid
secretKey = os.environ.get('baidu_secretKey')  # 你的密钥

## see lang ref: procs-translate.md
def translate(q, from_lang, to_lang):
    import hashlib
    # import urllib
    import urllib.parse
    import http.client
    import random
    import json
    import requests

    # httpClient = None
    myurl = '/api/trans/vip/translate'
    # q = 'apple'
    # q = 'I am a teacher'
    # q = '我是老师'
    # fromLang = 'en'
    # fromLang = 'zh'
    # fromLang = 'auto'
    # toLang = 'zh'
    # toLang = 'de'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    # m1 = md5.new()
    m1 = hashlib.md5()
    # m1.update(sign)
    # m1.update(sign.encode(encoding='iso8859-1'))
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        # httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        # httpClient.request('GET', myurl)
        # # response是HTTPResponse对象
        # response = httpClient.getresponse()
        # result = response.read()

        response=requests.get(url='http://api.fanyi.baidu.com'+myurl)
        if response.status_code == 200:
            result = response.json()
            # print(result)
            # data = json.loads(result)
            return result["trans_result"]
        return []
    except Exception as e:
        print(e)
        return []
    # finally:
    #     if httpClient:
    #         httpClient.close()

lang_mappings={
    'en':'en',
    'zh':'zh',
    'zh-CN':'zh',
    "de":'de',
    'ja':'jp',
    'es':'spa',
    'fr':'fra',
    'vi':'vie',
    'ko':'kor',
    'ru':'ru',
    'pt':'pt',
    'it':'it',
    'el':'el',
}

class BaiduTranslator(object):
    def trans(self, s, t, q):
        return translate(q, lang_mappings[s], lang_mappings[t])

    def to_zh(self, s, t, q):
        """
        $ python -m sagas.nlu.baidu_translator to_zh en zh "tom is a bad student"
            [{'src': 'tom is a bad student', 'dst': '汤姆是个坏学生'}]
        $ python -m sagas.nlu.baidu_translator to_zh en ja "tom is a bad student"
        $ python -m sagas.nlu.baidu_translator to_zh vi zh "Cậu bé uống nước ép."
        :return:
        """
        result = translate(q, lang_mappings[s], lang_mappings[t])
        print(result)

if __name__ == '__main__':
    import fire
    fire.Fire(BaiduTranslator)
