from typing import List, Any, Mapping, Optional

import faust

class CoResult(faust.Record):
    code: str
    data: faust.Record

class CoData(faust.Record):
    data: Any

class CoList(faust.Record):
    data: List[Any]
    notation: str = ''

class SrlVerb(faust.Record):
    verb: str
    description: str
    tags: List[str]

class SrlReform(faust.Record):
    verbs: List[SrlVerb]
    words: List[str]
    pos: Optional[List[str]]
    entities: Optional[List[str]]

class CoReforms(faust.Record):
    list: List[faust.Record]
    notation: str = ''

class PosReform(faust.Record):
    words: List[str]
    pos: List[str]

class DeppReform(PosReform):
    relations: List[str]
    heads: List[str]
    tree: Optional[Mapping]

