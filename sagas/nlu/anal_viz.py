from typing import Text, Any, Dict, List, Union, Optional
from sagas.nlu.anal import Doc

class AnalViz(object):
    """
    >>> f.doc._.graph()
    """
    def process(self, doc:Doc) -> bool:
        def render():
            from sagas.tracker_jupyter import enable_jupyter_tracker
            from sagas.nlu.uni_viz import EnhancedViz
            cv = EnhancedViz(shape='egg', size='8,5', fontsize=20)
            enable_jupyter_tracker()
            graph=cv.analyse_doc(doc.doc, None, console=False)
            return graph
        doc._.set('graph', lambda: render())
        return True

    @property
    def support_langs(self) -> Union[str, List[Text]]:
        return '*'


