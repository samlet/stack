from typing import List, Any
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

