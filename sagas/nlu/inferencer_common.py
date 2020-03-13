from typing import Text, Any, Dict, List, Union

from sagas.nlu.inferencer import InferPart


def get_all_plains(results: List[Any], expr) -> List[Text]:
    from jsonpath_ng.ext import parse
    jsonpath_expr = parse(expr)
    return [match.value for match in jsonpath_expr.find(results)]

def predict_pos(c:InferPart, t:Text, arg):
    pat = c.domain.pattern(t)
    r=pat(**{c.name:arg})
    if r[1]:
        return [(4, f"extract_for('plain', '{c.name}')"),
                (2, f"{c.name}='{arg}')")]

