# tts_utils.py
import pyttsx3
## ⊕ [langdetect · PyPI](https://pypi.org/project/langdetect/)
# from langdetect import detect
## ⊕ [polyglot · PyPI](https://pypi.org/project/polyglot/)
import polyglot
from polyglot.text import Text, Word

def say_with(sentence, voicekind):
    engine = pyttsx3.init()
    engine.setProperty("voice", voicekind)
    engine.say(sentence)
    engine.runAndWait()

def say_ja(sentence):
    say_with(sentence, "com.apple.speech.synthesis.voice.kyoko")

def say_lang(sentence, lang):
    """
    import sagas.nlu.tts_utils as tts
    tts.say_lang("私はサッカーをします", 'ja')
    :param sentence:
    :param lang:
    :return:
    """
    print("speak language with "+lang+" ...")
    # langdetect supports 55 languages out of the box ([ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)):
    # af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw

    if lang=="en":
        say_with(sentence, "com.apple.speech.synthesis.voice.daniel")
    elif lang=="es":
        # say_with(sentence, "com.apple.speech.synthesis.voice.monica")    
        # use es_MX, Paulina
        say_with(sentence, "com.apple.speech.synthesis.voice.paulina")  
    elif lang=="zh-tw":
        say_with(sentence, "com.apple.speech.synthesis.voice.mei-jia")
    elif lang.startswith("zh"):
        say_with(sentence, "com.apple.speech.synthesis.voice.ting-ting.premium") 
    ## com.apple.speech.synthesis.voice.anna ['de_DE']
    ## com.apple.speech.synthesis.voice.thomas ['fr_FR']
    elif lang=="fr":
        say_with(sentence, "com.apple.speech.synthesis.voice.thomas")
    elif lang=="de":
        say_with(sentence, "com.apple.speech.synthesis.voice.anna")
    elif lang=="ja":
        say_with(sentence, "com.apple.speech.synthesis.voice.kyoko")
    else:
        say_with(sentence, "com.apple.speech.synthesis.voice.kyoko")

    print('done.')

def say(sentence):
    # lang=detect(sentence)
    text = Text(sentence)
    print("Language Detected: Code={}, Name={}".format(text.language.code, text.language.name))
    lang=text.language.code
    say_lang(sentence, lang)

if __name__ == '__main__':
    say("Welcome to China.")
    say("私はサッカーをします")
    say("¿Dónde almorzamos hoy ?")
    say("C'est quoi cette chose ?")
    say("Ich gehe nicht.")
    # say("太平洋西北側的島嶼")
    say("在17世纪汉族移入前即已在此定居")


