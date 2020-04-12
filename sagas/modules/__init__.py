from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass

class agent_base(object):
    def __init__(self, ds):
        self.ds = ds

@dataclass
class ds_meta:
    agent: Any
    cond: List[Any]

_global_meta_ls=[]
def registry_meta_ls(meta_ls):
    _global_meta_ls.extend(meta_ls)

def global_meta_ls():
    return _global_meta_ls

