import requests
import json
from bs4 import BeautifulSoup
## $ pip install PyExecJS
import execjs #必须，需要先用pip 安装，用来执行js脚本

class Py4Js():
  def __init__(self):
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
  def getTk(self,text):
      return self.ctx.call("TL",text)

js = Py4Js()

def buildUrl(text,tk, source='auto', target='zh-CN'):
  baseUrl='https://translate.google.cn/translate_a/single'
  baseUrl+='?client=t&'

  # baseUrl+='s1=auto&'
  baseUrl += 'sl=%s&'%source
  # baseUrl+='t1=zh-CN&'
  baseUrl += 'tl=%s&' % target
  # baseUrl+='h1=zh-CN&'
  baseUrl += 'hl=en&'

  baseUrl+='dt=at&'
  baseUrl+='dt=bd&'
  baseUrl+='dt=ex&'
  baseUrl+='dt=ld&'
  baseUrl+='dt=md&'
  baseUrl+='dt=qca&'
  baseUrl+='dt=rw&'
  baseUrl+='dt=rm&'
  baseUrl+='dt=ss&'
  baseUrl+='dt=t&'
  baseUrl+='ie=UTF-8&'
  baseUrl+='oe=UTF-8&'
  baseUrl+='otf=1&'
  baseUrl+='pc=1&'
  baseUrl+='ssel=0&'
  baseUrl+='tsel=0&'
  baseUrl+='kc=2&'
  baseUrl+='tk='+str(tk)+'&'
  baseUrl+='q='+text
  return baseUrl

def join_sentence(r):
    rs=[]
    for sent in r[0]:
        if sent[0] is not None:
            # print('%s ✔ %s' % (sent[0], sent[1]))
            rs.append(sent[0])
    return ' '.join(rs)

def translations_df(trans):
    import sagas
    # fill with default field names
    size = len(trans[0][2][0])
    # print('size', size)
    listOfStrings = ['ext_' + str(i) for i in range(size)]
    if size==2:
        listOfStrings[0:2] = ['word', 'translations']
    else:
        listOfStrings[0:4] = ['word', 'translations', 'c', 'freq']

    return sagas.to_df(trans[0][2], listOfStrings)

def display_translations(trans):
    from tabulate import tabulate
    print(tabulate(translations_df(trans), headers='keys', tablefmt='psql'))

class TransTracker(object):
    def __init__(self):
        self.pronounce=[]
        # word translations as a pandas dataframe
        self.translations=None

def process_result(r, trans_verbose, options, tracker:TransTracker):
    import sagas
    if trans_verbose:
        print('❶ total result', len(r))
        for rl in r:
            print("♥", rl)
        print('--------------------------')
        # print(r[0])
        print('❷ total sents', len(r[0]))
        for sent in r[0]:
            print('❣', sent)
        if r[1] is not None:
            print('② translations for word')
            # print(r[1])
            display_translations(r[1])

        print('--------------------------')
        print('❸ tidy lines')
        for sent in r[0]:
            if sent[0] is not None:
                print('%s ✔ %s'%(sent[0], sent[1]))
            else:
                # pronounces
                for pr in sent:
                    if pr is not None:
                        print('ﺴ', pr)
        print('✁-------------------------')

    if 'get_pronounce' in options:
        for sent in r[0]:
            if sent[0] is None:
                for pr in sent:
                    if pr is not None:
                        # print('ﺴ', pr)
                        tracker.pronounce.append('❣ '+pr)
    if 'get_translations' in options:
        if r[1] is not None:
            trans=r[1]
            # tracker.translations=sagas.to_df(trans[0][2], ['word', 'translations', 'c', 'freq'])
            tracker.translations =translations_df(trans)

def translate(text, source='auto', target='zh-CN', trans_verbose=False, options=None):
  if options is None:
      options = {}
  tracker=TransTracker()

  header={
    'authority':'translate.google.cn',
    'method':'GET',
    'path':'',
    'scheme':'https',
    'accept':'*/*',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':'',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64)  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
'x-client-data':'CIa2yQEIpbbJAQjBtskBCPqcygEIqZ3KAQioo8oBGJGjygE='
  }
  url=buildUrl(text,js.getTk(text), source, target)
  res=''
  try:
      r=requests.get(url)
      result=json.loads(r.text)
      if result[7]!=None:
      # 如果我们文本输错，提示你是不是要找xxx的话，那么重新把xxx正确的翻译之后返回
          try:
              correctText=result[7][0].replace('<b><i>',' ').replace('</i></b>','')
              print(correctText)
              correctUrl=buildUrl(correctText,js.getTk(correctText), source, target)
              correctR=requests.get(correctUrl)
              newResult=json.loads(correctR.text)
              # res=newResult[0][0][0]
              res=join_sentence(newResult)

              process_result(newResult, trans_verbose, options, tracker)
          except Exception as e:
              print(e)
              # res=result[0][0][0]
              res = join_sentence(result)
      else:
          process_result(result, trans_verbose, options, tracker)
          # res=result[0][0][0]
          res = join_sentence(result)
  except Exception as e:
      res=''
      # print(url)
      print("翻译"+text+"失败")
      print("错误信息:", e)
  finally:
      return res, tracker

class GoogleTranslator(object):
    def translate(self, text, target='zh-CN', source='auto', verbose=False):
        """
        $ python -m sagas.nlu.google_translator translate 'Садись, где хочешь.'
        $ python -m sagas.nlu.google_translator translate 'Садись, где хочешь.' en
        $ python -m sagas.nlu.google_translator translate 'Садись, где хочешь.' en ru

        # multi-sentences
        $ python -m sagas.nlu.google_translator translate 'Что в этом конверте? Письмо и фотографии.' ja auto True
        $ python -m sagas.nlu.google_translator translate 'Что в этом конверте? Письмо и фотографии.' en auto True
        $ python -m sagas.nlu.google_translator translate 'I am a student.' ar en True

        $ python -m sagas.nlu.google_translator translate 'I have two refrigerators' th en True
        $ python -m sagas.nlu.google_translator translate 'I have two refrigerators' iw en True

        # word translations
        $ python -m sagas.nlu.google_translator translate 'city' ar en True
        $ python -m sagas.nlu.google_translator translate 'tiger' lo en True
        :param text:
        :return:
        """
        # trans_verbose=verbose
        res,_ = translate(text, source=source, target=target,
                        trans_verbose=verbose)
        print(res)
        # print(translate('Садись, где хочешь.'))
        # print(translate('I am a student.'))

    def trans_en(self, text, target='zh-CN'):
        """
        $ python -m sagas.nlu.google_translator trans_en 'I have two refrigerators' es
        :param text:
        :param target:
        :return:
        """
        self.translate(text, source='en', target=target, verbose=True)

if __name__ == '__main__':
  import fire
  fire.Fire(GoogleTranslator)


