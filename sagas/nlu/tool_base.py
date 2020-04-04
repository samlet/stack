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

    def doc_tree(self):
        from sagas.nlu.anal import build_anal_tree
        from anytree import Node, RenderTree, AsciiStyle, Walker, Resolver
        sents, lang, engine=self.meta.sents, self.meta.lang, self.meta.engine
        tree_root = build_anal_tree(sents, lang, engine)
        def additional(n):
            if n.upos=='VERB':
                return n.personal_pronoun_repr
            return ''
        print(RenderTree(tree_root, style=AsciiStyle()).by_attr(lambda n: f"{n.dependency_relation}: {n.text} ({n.upos.lower()}) {additional(n)}"))

    def execute(self):
        super().execute()
        self.doc_tree()
