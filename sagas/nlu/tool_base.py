from typing import Text, Dict, Any

from sagas.nlu.patterns import DefaultArgs
from sagas.nlu.rules_header import *
from sagas.nlu.registries import sinkers_fn

import sagas.tracker_fn as tc
from sagas.conf.conf import cf
import logging

logger = logging.getLogger(__name__)


class LangToolBase(LangSpecBase):
    def root_tree(self):
        from sagas.nlu.nlu_tools import vis_tree
        from sagas.nlu.ruleset_procs import cached_chunks
        chunks = cached_chunks(self.meta.sents,
                               source=self.meta.lang,
                               engine=self.meta.engine)
        tc.emp('cyan', f"✁ root tree {self.meta.engine} {'-' * 25}")
        ds=chunks['root_domains'][0]
        vis_tree(ds, self.meta.lang, trans=cf.is_enabled('trans_tree'))

    def execute(self):
        from sagas.nlu.anal_corpus import AnalCorpus
        super().execute()
        AnalCorpus().descrip(self.meta.sents,
                             self.meta.lang,
                             self.meta.engine)
