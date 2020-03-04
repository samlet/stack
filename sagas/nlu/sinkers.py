from typing import Text, Any, Dict, List, Union
import logging

from sagas.nlu.registries import sinkers_fn

logger = logging.getLogger(__name__)

class Sinkers(object):
    def __init__(self, data):
        self.mods=[]
        self.data=data

    def _process(self, results:List[Any]):
        for proc in sinkers_fn:
            proc(results, self.data)

    def add_module_results(self, mod_rs: Dict[Text, Any]):
        self.mods.append(mod_rs)

    def process_with_sinkers(self):
        all_rs = []
        for mod_rs in self.mods:
            for mod, matched in mod_rs.items():
                for ctx in matched.values():  # matched value type is Context
                    all_rs.extend(ctx.results)

        self._process(all_rs)



