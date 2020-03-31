from typing import Text, Any, Dict, List, Set, Union, Optional
from dataclasses import dataclass
import string
import logging
logger = logging.getLogger(__name__)


@dataclass
class token:
    value: str
    children: Optional[Dict[Text, 'token']]


class PatternFormatter(string.Formatter):
    def format_field(self, value, spec):
        if spec == '_':
            return value.value
        elif spec.startswith('/'):
            return value.children[spec[1:]].value
        else:
            return super(PatternFormatter, self).format_field(value, spec)

def get_descriptor_from_result(result, expr) -> List[Text]:
    from jsonpath_ng.ext import parse
    jsonpath_expr = parse(expr)
    return next((match.value for match in jsonpath_expr.find(result)), None)

def set_val(var_map, part, val):
    import re
    if ':' in part:
        domain, part, sub=re.split('[:/]', part)
        if part not in var_map:
            var_map[part]=token('', children={sub:token(val,{})})
        else:
            var_map[part].children[sub]=token(val, {})
    else:
        if part not in var_map:
            var_map[part]=token(val, {})
        else:
            var_map[part].value=val

descriptors={'specs_of': '$.value.category',
             'kind_of': '$.value.category',
             'pipes': '$.value[*].value',
            }

class ResultsRender(object):
    """
    >>> from sagas.nlu.results_render import ResultsRender
    >>> dsp = ResultsRender()
    >>> patt = 'behave {obj:_} for {obj:/obj}, modal {_:_}'
    >>> tc.emp('magenta', dsp.render(patt, results))
    """
    def render(self, patt:Text, results:List[Any]) -> Text:
        pf = PatternFormatter()
        var_map = {}
        for rs in results:
            ins = rs['inspector']
            part = rs['part']
            if ins in descriptors:
                expr = descriptors[ins]
                val = get_descriptor_from_result(rs, expr)
                if val:
                    set_val(var_map, part, val)
                else:
                    logger.warning(f'absent val: {expr}')

        return pf.format(patt, **var_map)

    def build(self, results:List[Any]) -> Dict[Text, Text]:
        all_pats = set([r['pattern'] for r in results if '{' in r['pattern']])
        render_map={}
        for pat in all_pats:
            rs = [r for r in results if r['pattern'] == pat]
            render_map[pat]=self.render(pat, rs)
        return render_map

