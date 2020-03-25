import stanza

langs_models={}

def get_nlp(lang):
    alias={'zh':'zh-hans', 'no':'nb'}
    if lang not in langs_models:
        langs_models[lang]= stanza.Pipeline(dir='/pi/ai/corenlp/1.0',
                                            package='default',
                                            lang=alias[lang] if lang in alias else lang)
    return langs_models[lang]

