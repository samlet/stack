from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass
from sagas.conf.conf import cf

# class agent_base(object):
#     def __init__(self, ds):
#         self.ds = ds

@dataclass
class ds_meta:
    ds: Any  # has name property
    cond: List[Any]

_global_meta_ls=[]
def registry_meta_ls(*meta_ls):
    _global_meta_ls.extend([m for m in meta_ls if m not in _global_meta_ls])

def init_agents():
    ins=[c() for c in cf.classes('agents')]
    registry_meta_ls(*ins)

def global_meta_ls():
    return _global_meta_ls

def match_agent(target, agent, verbose=False):
    import sagas.tracker_fn as tc
    rset = [(cond, target.match(cond)) for cond in agent.meta.cond]
    succ=all([r for c, r in rset])
    if verbose:
        tc.emp('green' if succ else 'white', '✔' if succ else '✘',
               agent.meta.ds.name, rset)
    return succ

def match_agents(target):
    rs=[]
    for m in global_meta_ls():
        if match_agent(target, m):
            rs.append(m)
    return rs

init_agents()

