from typing import Text, Any, Dict, List, Union, Optional
import stanza
from cachetools import cached

from sagas.conf.conf import cf

@cached(cache={})
def get_nlp(lang:Text, package:Text='default', processors:Text=None,
            pretokenized:bool=False):
    processors = processors or {}
    alias={'zh':'zh-hans', 'no':'nb'}
    packages={'pl':'pdb'}
    return stanza.Pipeline(dir=f'{cf.conf_dir}/ai/corenlp/1.0',
                           package=packages[lang] if lang in packages else package,
                           processors=processors,
                           lang=alias[lang] if lang in alias else lang,
                           tokenize_pretokenized=pretokenized
                           )

