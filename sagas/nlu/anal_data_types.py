from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass

class ConstType(object):
    def __init__(self, val):
        self.val=val
    def __repr__(self):
        return self.val
    def __str__(self):
        return self.val

_ = ANY = ConstType('_')
PredCond=Union[str, ConstType, 'behave_', 'desc_']

class path_(object):
    val: str
    cond: Optional[PredCond]

    def __init__(self, val):
        self.val = val
        self.cond=None

    def __eq__(self, cond):
        self.cond = cond
        return self

    def __repr__(self):
        return f'path: {self.val} -> {type(self.cond).__name__}'

    def __str__(self):
        return self.__repr__()

class rel_(path_):
    def __repr__(self):
        return f'path: {self.val} -> {type(self.cond).__name__}'

class pos_(path_):
    def __repr__(self):
        return f'path: {self.val} -> {type(self.cond).__name__}'

@dataclass
class base_model_(object):
    ops: List[Tuple]
    flags: Tuple[path_, ...]

    def __init__(self, *flags):
        self.flags=flags

    def __and__(self, other):
        self.ops.append(('and', other))
        return self

    def __or__(self, other):
        self.ops.append(('or', other))
        return self

@dataclass
class behave_(base_model_):
    subj: PredCond
    obj: PredCond
    iobj: PredCond
    behave: PredCond

    def __init__(self, subj, behave, obj, iobj=_, *flags):
        super().__init__(*flags)
        self.subj = subj
        self.obj = obj
        self.iobj = iobj
        self.behave = behave
        self.ops = []

@dataclass
class desc_(base_model_):
    subj: PredCond
    aux: PredCond
    desc: PredCond
    flags: Dict[Text, Any]

    def __init__(self, subj, desc, aux=_, *flags):
        super().__init__(*flags)
        self.subj=subj
        self.desc=desc
        self.aux=aux

@dataclass
class phrase_(base_model_):
    head: PredCond
    flags: Dict[Text, Any]

    def __init__(self, head, *flags):
        super().__init__(*flags)
        self.head = head

