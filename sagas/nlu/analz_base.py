from typing import Text, Any, Dict, List, Union, Optional, Tuple
from dataclasses import dataclass

@dataclass
class Docz:
    words: List
    postags: List
    arcs: List
    roles: List
    netags: List
    terms: List[Dict[Text,Text]]

