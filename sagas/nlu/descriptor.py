from typing import Text, Any, Dict, List, Set, Union, Optional
from dataclasses import dataclass
import string
import logging

logger = logging.getLogger(__name__)

@dataclass
class token:
    value: str

    def __getattr__(self, name):
        if self.value.endswith(':'):
            return token(value=self.value + name)
        return token(value=self.value + '/' + name)

def get_descriptor(result, expr) -> List[Text]:
    from jsonpath_ng.ext import parse
    jsonpath_expr = parse(expr)
    return [match.value for match in jsonpath_expr.find(result)]
def get_personal_pronoun(results, part:Text):
    ins_cond=f'$[?inspector = "extract_comps" & provider = "feats" & part="{part}"]'
    return get_descriptor(results, ins_cond+'.value[*].Person,Number')

def digest_cat(results, part):
    # print(part, results)
    for ins in ['specs_of', 'kind_of']:
        ins_cond = f'$[?inspector = "{ins}" & part="{part}"]'
        vals = get_descriptor(results, ins_cond + '.value.category')
        if vals:
            return vals[0]

    ins_cond = f'$[?inspector = "pipes" & part="{part}"]'
    vals = get_descriptor(results, ins_cond + '.value[*].value')
    return vals[0] if vals else None


def digest(results, path, spec):
    fn = {'cat': digest_cat,
          'personal': get_personal_pronoun,
          }
    ret = fn[spec](results, path)
    logger.debug('.. digest %s, %s, %s', path, spec, ret)
    return ret


class PatternDescriptor(string.Formatter):
    def __init__(self, results):
        self.results = results
        self.values=[]

    def format_field(self, value:token, spec:Text):
        val = digest(self.results, value.value, spec)
        self.values.append({'path':value.value, 'spec':spec, 'value':val})
        if isinstance(val, list):
            val = '_'.join(val)
        return val if val else '_'

class Descriptor(object):
    def __init__(self):
        self.value_map={}

    def create_values(self, values:List[Any], patt:Text):
        import re
        raw = re.sub(r" ?{[^{]+\}", "|", patt)
        logger.debug(raw)
        name_list = raw.replace(',', '').split('|')
        names=[name.strip() for name in name_list if name]
        self.value_map[patt]=dict(zip(names, values))

    def render(self, patt: Text, results: List[Any]) -> Text:
        logger.debug(f"process {patt}")
        pf = PatternDescriptor(results)
        ctx={key:token(key+':') for key in ('verb', 'aux', 'subj', 'root', 'predicts', '_')}
        r=pf.format(patt, **ctx)
        self.create_values(pf.values, patt)
        return r

    def build(self, results: List[Any]) -> Dict[Text, Text]:
        all_pats = set([r['pattern'] for r in results if '{' in r['pattern']])
        logger.debug(f"total patterns {len(all_pats)}")
        render_map = {}
        for pat in all_pats:
            rs = [r for r in results if r['pattern'] == pat]
            render_map[pat] = self.render(pat, rs)
        return render_map


