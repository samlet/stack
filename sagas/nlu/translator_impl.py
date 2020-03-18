from typing import Text, Any, Dict, List, Union, Set
import requests
import json

import logging

from sagas.nlu.translator_intf import join_sentence, TransTracker, TranslatorIntf

logger = logging.getLogger(__name__)


class Py4Js():
    def __init__(self):
        import execjs
        self.ctx = execjs.compile(""" 
        function TL(a) { 
        var k = ""; 
        var b = 406644; 
        var b1 = 3293161072;       
        var jd = "."; 
        var $b = "+-a^+6"; 
        var Zb = "+-3^+b+-f";    
        for (var e = [], f = 0, g = 0; g < a.length; g++) { 
            var m = a.charCodeAt(g); 
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023), 
            e[f++] = m >> 18 | 240, 
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224, 
            e[f++] = m >> 6 & 63 | 128), 
            e[f++] = m & 63 | 128) 
        } 
        a = b; 
        for (f = 0; f < e.length; f++) a += e[f], 
        a = RL(a, $b); 
        a = RL(a, Zb); 
        a ^= b1 || 0; 
        0 > a && (a = (a & 2147483647) + 2147483648); 
        a %= 1E6; 
        return a.toString() + jd + (a ^ b) 
      };      
      function RL(a, b) { 
        var t = "a"; 
        var Yb = "+"; 
        for (var c = 0; c < b.length - 2; c += 3) { 
            var d = b.charAt(c + 2), 
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d), 
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d; 
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d 
        } 
        return a 
      } 
     """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


js = Py4Js()

def buildUrl(text,tk, source='auto', target='zh-CN'):
    baseUrl = 'https://translate.google.cn/translate_a/single'
    baseUrl += '?client=t&'

    # baseUrl+='s1=auto&'
    baseUrl += 'sl=%s&' % source
    # baseUrl+='t1=zh-CN&'
    baseUrl += 'tl=%s&' % target
    # baseUrl+='h1=zh-CN&'
    baseUrl += 'hl=en&'

    baseUrl += 'dt=at&'
    baseUrl += 'dt=bd&'
    baseUrl += 'dt=ex&'
    baseUrl += 'dt=ld&'
    baseUrl += 'dt=md&'
    baseUrl += 'dt=qca&'
    baseUrl += 'dt=rw&'
    baseUrl += 'dt=rm&'
    baseUrl += 'dt=ss&'
    baseUrl += 'dt=t&'
    baseUrl += 'ie=UTF-8&'
    baseUrl += 'oe=UTF-8&'
    baseUrl += 'otf=1&'
    baseUrl += 'pc=1&'
    baseUrl += 'ssel=0&'
    baseUrl += 'tsel=0&'
    baseUrl += 'kc=2&'
    baseUrl += 'tk=' + str(tk) + '&'
    baseUrl += 'q=' + text

    return baseUrl

class TranslatorImpl(TranslatorIntf):
    def execute(self, text:Text, source:Text, target:Text,
                trans_verbose, options:Set[Text],
                tracker:TransTracker, process_result) -> Text:
        header = {
            'authority': 'translate.google.cn',
            'method': 'GET',
            'path': '',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
            'x-client-data': 'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
        }
        url = buildUrl(text, js.getTk(text), source, target)

        meta = {'text': text, 'source': source, 'target': target}
        res = ''
        try:
            r = requests.get(url, headers=header, timeout=1.5)
            result = json.loads(r.text)
            # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
            # if result[7]!=None:
            if result[7] is not None and 'disable_correct' not in options:
                try:
                    correctText = result[7][0].replace('<b><i>', ' ').replace('</i></b>', '')
                    print(correctText)
                    correctUrl = buildUrl(correctText, js.getTk(correctText), source, target)
                    correctR = requests.get(correctUrl)
                    newResult = json.loads(correctR.text)
                    # res=newResult[0][0][0]
                    res = join_sentence(newResult)

                    process_result(meta, newResult, trans_verbose, options, tracker)
                except Exception as e:
                    # print('translate error: ', e, f", in process text {text}")
                    # res=result[0][0][0]
                    res = join_sentence(result)
                    process_result(meta, result, trans_verbose, options, tracker)
            else:
                process_result(meta, result, trans_verbose, options, tracker)
                # res=result[0][0][0]
                res = join_sentence(result)


        except Exception as e:
            res = ''
            logger.error("translate fail: " + text)
            logger.error("error message: %s", e)
        finally:
            return res
