from typing import Text, Any, Dict, List, Union
import logging
logger = logging.getLogger(__name__)

class Sinkers(object):
    def __init__(self):
        def tags(results:List[Any]):
            val_list=[r['value'] for r in results if r['inspector'] == 'tags']
            all_tags=set([item for sublist in val_list for item in sublist])

            logger.info(f"tags: {all_tags}")

        self.procs=[tags]
        self.mods=[]

    def _process(self, results:List[Any]):
        for proc in self.procs:
            proc(results)

    def add_module_results(self, mod_rs: Dict[Text, Any]):
        self.mods.append(mod_rs)

    def process_with_sinkers(self):
        all_rs = []
        for mod_rs in self.mods:
            for mod, matched in mod_rs.items():
                for ctx in matched.values():  # matched value type is Context
                    all_rs.extend(ctx.results)

        self._process(all_rs)



