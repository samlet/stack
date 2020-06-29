from typing import Text, Any, Dict, List, Union, Optional
import logging

from sagas import AttrDict
from sagas.listings.co_data import CoResult
from sagas.listings.co_intf import BaseConf, BaseCo
from sagas.listings.co_data import SrlReform, CoReforms, SrlVerb
import os, torch
from ltp import LTP
from ltp.ltp import no_gard

logger = logging.getLogger(__name__)

def norm_arg(tag, lead='B'):
    if len(tag)==2 and tag[0]=='A':
        return f"{lead}-ARG{tag[1]}"
    return f"{lead}-{tag}"

class LtpExt(LTP):
    @no_gard
    def ner_bio(self, hidden: dict):
        word_length = torch.as_tensor(hidden['word_length'], device=self.device)
        ner_output = self.model.ner_decoder(hidden['word_input'], word_length)
        ner_output = torch.argmax(ner_output, dim=-1).cpu().numpy()
        ner_output = self._convert_idx_to_name(ner_output, hidden['word_length'], self.ner_vocab)
        # return [get_entities(ner) for ner in ner_output]
        return ner_output

class LtpSrlCo(BaseCo):
    def preload(self):
        self.ltp = LtpExt()

    def build_reform(self, seg, srl):
        reform = SrlReform(words=seg, verbs=[])
        for i, (tok, term) in enumerate(zip(seg, srl)):
            # print(tok, term)
            if not term:
                continue

            placers = ['O'] * len(seg)
            for tag, start, end in term:
                for p in range(start, end + 1): placers[p] = norm_arg(tag, 'I')
                placers[start] = norm_arg(tag)
                # print('\t', tag, ":", "".join(seg[start:end + 1]))
            placers[i] = 'B-V'
            # print('\t', placers)
            verb_form = SrlVerb(verb=tok, description='', tags=placers)
            reform.verbs.append(verb_form)
        return reform

    def proc(self, conf:AttrDict, input:Any) -> CoResult:
        ls = input if isinstance(input, List) else input['sents']
        sents = self.ltp.sent_split(ls)
        segs, hidden = self.ltp.seg(sents)
        srls = self.ltp.srl(hidden)
        reforms=CoReforms(list=[])
        for seg, srl in zip(segs, srls):
            reform=self.build_reform(seg, srl)
            reforms.list.append(reform)

        if 'pos' in conf.pipelines:
            pos_ls=self.ltp.pos(hidden)
            for reform, pos in zip(reforms.list, pos_ls):
                reform.pos=pos

        if 'ner' in conf.pipelines:
            ners=self.ltp.ner_bio(hidden)
            for reform, ner in zip(reforms.list, ners):
                reform.entities=ner

        return CoResult(code='ok', data=reforms)

