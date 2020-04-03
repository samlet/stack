import stanza
from sagas.conf.conf import cf

langs_models={}

def get_nlp(lang, package='default', processors=None):
    processors = processors or {}
    alias={'zh':'zh-hans', 'no':'nb'}
    packages={'pl':'pdb'}
    if lang not in langs_models:
        langs_models[lang]= stanza.Pipeline(dir=f'{cf.conf_dir}/ai/corenlp/1.0',
                                            package=packages[lang] if lang in packages else package,
                                            processors=processors,
                                            lang=alias[lang] if lang in alias else lang)
    return langs_models[lang]

