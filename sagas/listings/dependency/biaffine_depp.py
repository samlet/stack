from typing import Text, Any, Dict, List, Union, Optional
import logging
from sagas.conf.conf import cf
from sagas.listings.co_data import CoResult, DeppReform
from sagas.listings.co_intf import BaseConf, BaseCo

logger = logging.getLogger(__name__)


class DeppConf(BaseConf):
    model = ''


class BiaffineDeppCo(BaseCo):
    def __init__(self, conf):
        self.conf = DeppConf(**conf)

    def preload(self):
        from allennlp_models.structured_prediction import BiaffineDependencyParserPredictor
        self.predictor_depp = BiaffineDependencyParserPredictor.from_path(f"{cf.data_dir}/allenai/biaffine-dependency-parser-ptb-2020.04.06.tar.gz")

    def proc(self, input: Any) -> CoResult:
        sentence = input if isinstance(input, str) else input['sentence']
        r = self.predictor_depp.predict(sentence=sentence)
        reform = DeppReform(words=r['words'],
                            pos=r['pos'],
                            relations=r['predicted_dependencies'],
                            heads=r['predicted_heads'],
                            tree=r['hierplane_tree']
                            )
        return CoResult(code='ok', data=reform)

class DeppVisualizer(object):
    def render(self, reform):
        from anytree.importer import DictImporter
        from anytree import RenderTree

        importer = DictImporter()
        # tree_root = importer.import_(r['hierplane_tree']['root'])
        print([(w, h) for w, h in zip(reform.words, reform.heads)])
        tree_root = importer.import_(reform.tree['root'])
        tree = RenderTree(tree_root)
        for pre, fill, node in tree:
            print("%s%s: %s (%s)" % (pre, node.nodeType, node.word,
                                     ','.join(node.attributes).lower()))

