#! /usr/bin/env python
# -*- coding:utf-8 -*-

import urllib.request
import urllib.parse
import json
import execjs
import re
import time
import random

from sagas.nlu.google_translator import display_translations


class GoogleTrans(object):
    def __init__(self):
        self.url = 'https://translate.google.cn/translate_a/single'
        self.TKK = "434674.96463358"  # 随时都有可能需要更新的TKK值

        self.header = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "NID=188=M1p_rBfweeI_Z02d1MOSQ5abYsPfZogDrFjKwIUbmAr584bc9GBZkfDwKQ80cQCQC34zwD4ZYHFMUf4F59aDQLSc79_LcmsAihnW0Rsb1MjlzLNElWihv-8KByeDBblR2V1kjTSC8KnVMe32PNSJBQbvBKvgl4CTfzvaIEgkqss",
            "referer": "https://translate.google.cn/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
            "x-client-data": "CJK2yQEIpLbJAQjEtskBCKmdygEIqKPKAQi5pcoBCLGnygEI4qjKAQjxqcoBCJetygEIza3KAQ==",
        }

        self.data = {
            "client": "webapp",  # 基于网页访问服务器
            "sl": "auto",  # 源语言,auto表示由谷歌自动识别
            "tl": "en",  # 翻译的目标语言
            "hl": "zh-CN",  # 界面语言选中文，毕竟URL都是cn后缀了，就不装美国人了
            "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],  # dt表示要求服务器返回的数据类型
            "otf": "2",
            "ssel": "0",
            "tsel": "0",
            "kc": "1",
            "tk": "",  # 谷歌服务器会核对的token
            "q": ""  # 待翻译的字符串
        }

        with open('token.js', 'r', encoding='utf-8') as f:
            self.js_fun = execjs.compile(f.read())

    def update_TKK(self):
        url = "https://translate.google.cn/"

        req = urllib.request.Request(url=url, headers=self.header)
        page_source = urllib.request.urlopen(req).read().decode("utf-8")

        self.TKK = re.findall(r"tkk:'([0-9]+\.[0-9]+)'", page_source)[0]

    def construct_url(self):
        base = self.url + '?'
        for key in self.data:
            if isinstance(self.data[key], list):
                base = base + "dt=" + "&dt=".join(self.data[key]) + "&"
            else:
                base = base + key + '=' + self.data[key] + '&'
        base = base[:-1]
        return base

    def query(self, q, lang_from='', lang_to=''):
        self.data['q'] = urllib.parse.quote(q)
        self.data['tk'] = self.js_fun.call('wo', q, self.TKK)
        if lang_from:
            self.data['sl'] = lang_from
        if lang_to:
            self.data['tl'] = lang_to
        url = self.construct_url()
        req = urllib.request.Request(url=url, headers=self.header)
        response = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
        print(response[0][0][0])
        if response[1] is not None:
            print('.. translations for word')
            # print(r[1])
            display_translations(response[1])

class TransCli(object):
    def tests(self):
        """
        $ ./test_trans_2.py tests
        :return:
        """
        googletrans = GoogleTrans()
        googletrans.update_TKK()  # 构建完对象以后要同步更新一下TKK值
        time.sleep(random.uniform(0.05, 0.20))
        text = 'يىغلىمايۋاتىدۇ'
        googletrans.query(text, 'ug', 'en')  # 默认的目标语言是英语，如果要翻译到其他语言请自行修改相应参数

        time.sleep(random.uniform(0.05, 0.20))

        googletrans = GoogleTrans()
        googletrans.update_TKK()
        time.sleep(random.uniform(0.05, 0.20))
        googletrans.query('你好', 'zh', 'en')

    def trans(self, sents, lang):
        """
        $ ./test_trans_2.py trans 'Ontem nós fizemos almoço na minha padaria.' pt

        :param sents:
        :param lang:
        :return:
        """
        from urllib.error import URLError
        for n in range(3):
            try:
                googletrans = GoogleTrans()
                googletrans.update_TKK()
                # time.sleep(random.uniform(0.05, 0.20))
                googletrans.query(sents, lang, 'en')
                break
            except URLError:
                print('.. wait to retry')
                time.sleep(random.uniform(0.05, 0.20))
                continue

if __name__ == '__main__':
    import fire
    fire.Fire(TransCli)

