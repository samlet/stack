from typing import Text, Any, Dict, List, Union, Optional

from cachetools import cached
from graphql import graphql_sync
from ariadne import ObjectType, QueryType, make_executable_schema
from ariadne import make_executable_schema, load_schema_from_path, ObjectType, QueryType
import json

from sagas.nlu.anal_defs import vtable
from sagas.util.collection_util import wrap, to_obj
from sagas.nlu.utils import fix_sents
import pandas as pd
from sagas.nlu.anal import delegator
from sagas.nlu.anal_expr import match
from sagas.nlu.anal_data_types import behave_, desc_, phrase_, rel_, path_, _, _1, _2

@cached(cache={})
def get_corpus(lang:Text, chapter:Text):
    dfjson = pd.read_json(f'~/pi/stack/crawlers/langcrs/all_{lang}.json')
    ch=dfjson[dfjson['chapter'].str.match(chapter)]
    rs=[]
    for i, (sent,ref) in enumerate(zip(ch['translate'], ch['text'])):
        rs.append(fix_sents(sent, lang))
    return rs

def node_text(n):
    return n.text if n is not None else '_'

def wrap_behave(f_behave):
    return {'id':'0', 'subj':node_text(f_behave.subj),
            'obj':node_text(f_behave.obj),
            'iobj':node_text(f_behave.iobj),
            'behave':node_text(f_behave.behave),
            'behave_spec': f_behave.behave.spec() if f_behave.behave else '_',
            'obj_spec': f_behave.obj.spec() if f_behave.obj else '_',
           }

def resolve_behaves(bucket, info):
    results=[]
    for text in bucket.rs:
        f=delegator.f(text, bucket.lang)
        f_behave=f.as_behave()
        if f_behave:
            if bucket.routine(f, f_behave):
                results.append(wrap_behave(f_behave))
    return results

@vtable
def _study(f, f_behave):
    return match(f,
                 behave_(_, _1 << 'study|学习', _2 << _, _), lambda arg, *v: wrap_behave(f_behave),
                 behave_(_, _1 << 'study|学习', _, _), lambda arg, *v: wrap_behave(f_behave),
                 _, None)

def bucket_behaves(x, info, _id):
    # mappings={'study': _study}
    mappings=vtable.all
    return wrap(id=_id,
                routine=mappings[_id],
                lang='pt',
                rs=get_corpus('pt', 'At school')) if _id in mappings else None


class AnalQl(object):
    def __init__(self):
        from sagas.conf import resource_path
        self.type_defs = load_schema_from_path(resource_path('schemas.graphql'))
        query = QueryType()
        bucket = ObjectType('Bucket')
        behave = ObjectType('Behave')
        desc = ObjectType('Desc')

        query.set_field('bucket_behaves', bucket_behaves)
        bucket.set_field('behaves', resolve_behaves)
        self.schema = make_executable_schema(self.type_defs, [behave, bucket, query])

    def query_sync(self, q:Text):
        return graphql_sync(self.schema, q)

class AnalQlProcs(object):
    def bucket(self, id='study'):
        """
        $ python -m sagas.nlu.anal_ql bucket study
        :param id:
        :return:
        """
        rec = bucket_behaves(None, None, id)
        return resolve_behaves(rec, None)

    def testing(self):
        """
        $ python -m sagas.nlu.anal_ql testing
        :return:
        """
        from pprint import pprint
        q = """{
            bucket_behaves(_id:"study"){     
                id
                behaves {
                    subj
                    behave_spec
                    obj_spec
                }
            }
        }
        """

        anal_ql = AnalQl()
        result = anal_ql.query_sync(q)
        if not result.errors:
            pprint(result.data)
        else:
            pprint(result)

if __name__ == '__main__':
    import fire
    fire.Fire(AnalQlProcs)

