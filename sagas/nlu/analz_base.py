from typing import Text, Any, Dict, List, Union, Optional, Tuple
from dataclasses import dataclass

from sagas.nlu.anal_defs import terms_list


@dataclass
class Docz:
    words: List
    postags: List
    arcs: List
    roles: List
    netags: List
    terms: List[Dict[Text,Text]]

    def filter_terms(self) -> List[Dict[Text,Text]]:
        return list(filter(lambda x: x['term'] in terms_list, self.terms))

