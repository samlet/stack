# tts_utils.py
## ⊕ [langdetect · PyPI](https://pypi.org/project/langdetect/)
# from langdetect import detect
## ⊕ [polyglot · PyPI](https://pypi.org/project/polyglot/)

"""
preqs:
pip install pyobjc
pip install pyttsx3
"""
def say_with(sentence, voicekind):
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", voicekind)
    engine.say(sentence)
    engine.runAndWait()
    return engine

def say_ja(sentence):
    # say_with(sentence, "com.apple.speech.synthesis.voice.kyoko")
    return say_with(sentence, 'com.apple.speech.synthesis.voice.kyoko.premium')

def say_lang(sentence, lang, verbose=True):
    """
    import sagas.nlu.tts_utils as tts
    tts.say_lang("私はサッカーをします", 'ja')
    :param sentence:
    :param lang:
    :return:
    """
    import random
    if verbose:
        print("speak language with "+lang+" ...")
    # langdetect supports 55 languages out of the box ([ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)):
    # af, ar, bg, bn, ca, cs, cy, da, de, el, en, es, et, fa, fi, fr, gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, mk, ml, mr, ne, nl, no, pa, pl, pt, ro, ru, sk, sl, so, sq, sv, sw, ta, te, th, tl, tr, uk, ur, vi, zh-cn, zh-tw

    if lang=="en":
        say_with(sentence, "com.apple.speech.synthesis.voice.samantha.premium")
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
        say_with(sentence, "com.apple.speech.synthesis.voice.audrey.premium")
    elif lang=="de":
        say_with(sentence, "com.apple.speech.synthesis.voice.anna")
    elif lang=="ja":
        voices=['com.apple.speech.synthesis.voice.otoya.premium',
                'com.apple.speech.synthesis.voice.kyoko.premium']
        idx=random.randint(0,len(voices)-1)
        say_with(sentence, voices[idx])
        # say_with(sentence, "com.apple.speech.synthesis.voice.kyoko.premium")
        # say_with(sentence, "com.apple.speech.synthesis.voice.kyoko")
    elif lang=='it':
        say_with(sentence, 'com.apple.speech.synthesis.voice.luca')
    elif lang=='pt':
        say_with(sentence, 'com.apple.speech.synthesis.voice.joana')
    elif lang=='ru':
        say_with(sentence, 'com.apple.speech.synthesis.voice.milena.premium')
    elif lang=='ar':
        say_with(sentence, 'com.apple.speech.synthesis.voice.laila.premium')
    elif lang=='ko':
        say_with(sentence, 'com.apple.speech.synthesis.voice.yuna.premium')
    elif lang=='hi':
        say_with(sentence, 'com.apple.speech.synthesis.voice.lekha')
    elif lang=='he':
        say_with(sentence, 'com.apple.speech.synthesis.voice.carmit.premium')
    elif lang=='fi':
        say_with(sentence, 'com.apple.speech.synthesis.voice.satu.premium')
    elif lang=='tr':
        say_with(sentence, 'com.apple.speech.synthesis.voice.yelda')
    elif lang == 'pt':
        say_with(sentence, 'com.apple.speech.synthesis.voice.joana.premium')
    elif lang == 'id':
        say_with(sentence, 'com.apple.speech.synthesis.voice.damayanti.premium')
        # voice.damayanti.premium
    elif lang == 'el':
        say_with(sentence, 'com.apple.speech.synthesis.voice.melina.premium')
    else:
        # say_with(sentence, "com.apple.speech.synthesis.voice.kyoko")
        raise Exception(f'Not specific a voice for the language {lang}')

    if verbose:
        print('done.')

def say(sentence):
    import polyglot
    from polyglot.text import Text, Word
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


