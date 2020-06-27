from typing import Text, Any, List, Optional, Union, Dict

from sagas.listings.co_data import CoResult, CoList
from sagas.listings.co_intf import BaseConf, BaseCo


class T5Conf(BaseConf):
    prefix = 'translate English to German'

class T5Co(BaseCo):
    model: Any=None
    tokenizer: Any=None

    def __init__(self, conf):
        self.conf=T5Conf(**conf)

    def preload(self):
        from transformers import AutoModelWithLMHead, AutoTokenizer
        # if self.model is None or self.tokenizer is None:
        print('.. load model t5-base')
        self.model = AutoModelWithLMHead.from_pretrained("t5-base")
        self.tokenizer = AutoTokenizer.from_pretrained("t5-base")

    def proc(self, input:Any) -> CoResult:
        # self.preload()
        sentence=input if isinstance(input, str) else input['sentence']
        inputs = self.tokenizer.encode(
            f"{self.conf.prefix}: {sentence}",
            return_tensors="pt")
        outputs = self.model.generate(inputs, max_length=40, num_beams=4, early_stopping=True)
        result= [self.tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in outputs]
        return CoResult(code='ok', data=CoList(data=result))



