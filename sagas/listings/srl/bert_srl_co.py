from typing import Text, Any, Dict, List, Union, Optional
import allennlp.models
from sagas import AttrDict
from sagas.conf.conf import cf
from sagas.listings.co_data import SrlReform, CoResult
from sagas.listings.co_intf import BaseConf, BaseCo
import logging

logger = logging.getLogger(__name__)

def terms_tokens(terms: SrlReform):
    from sagas.nlu.utils import get_entities
    # words = terms.words
    rs = []
    for v in terms.verbs:
        verb=v.verb
        term_toks=get_entities(v.tags)
        tokens=[{'verb':verb, 'tag':tag, 'start':start, 'end':end} for tag,start,end in term_toks]
        rs.append(tokens)
    return rs

class BertSrlCo(BaseCo):
    def preload(self):
        from allennlp_models.structured_prediction import SemanticRoleLabelerPredictor
        logger.info('.. load bert-base-srl')
        self.predictor = SemanticRoleLabelerPredictor.from_path(f"{cf.data_dir}/allenai/bert-base-srl-2020.03.24.tar.gz")

    def proc(self, conf:AttrDict, input:Any) -> CoResult:
        sentence = input if isinstance(input, str) else input['sentence']
        r = self.predictor.predict(sentence=sentence)
        data= SrlReform.from_data(r)
        return CoResult(code='ok', data=data)

