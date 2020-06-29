from typing import Text, Any, Dict, List, Union, Optional
import logging

from sagas import AttrDict
from sagas.conf.conf import cf
from sagas.listings.co_data import CoResult, DeppReform
from sagas.listings.co_intf import BaseConf, BaseCo

logger = logging.getLogger(__name__)

class BiaffineDeppCo(BaseCo):
    def preload(self):
        from allennlp_models.structured_prediction import BiaffineDependencyParserPredictor
        self.predictor_depp = BiaffineDependencyParserPredictor.from_path(f"{cf.data_dir}/allenai/biaffine-dependency-parser-ptb-2020.04.06.tar.gz")

    def proc(self, conf:AttrDict, input:Any) -> CoResult:
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
    """
    >>> from sagas.listings.dependency.biaffine_depp import DeppVisualizer
    >>> import sagas
    >>> r = sagas.profs.depp.BiaffineDepp(sentence="Hugging Face is a technology company based in New York and Paris")
    >>> DeppVisualizer().render(r['data'])
    """
    def render(self, reform):
        from anytree.importer import DictImporter
        from anytree import RenderTree

        if isinstance(reform, dict):
            reform=DeppReform.from_data(reform)

        importer = DictImporter()
        # tree_root = importer.import_(r['hierplane_tree']['root'])
        print([(w, h) for w, h in zip(reform.words, reform.heads)])
        tree_root = importer.import_(reform.tree['root'])
        tree = RenderTree(tree_root)
        for pre, fill, node in tree:
            print("%s%s: %s (%s)" % (pre, node.nodeType, node.word,
                                     ','.join(node.attributes).lower()))

