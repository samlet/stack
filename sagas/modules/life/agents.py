from typing import Text, Any, Dict, List, Union, Optional, Tuple, Set
from dataclasses import dataclass

from sagas.modules import agent_base, ds_meta, registry_meta_ls, global_meta_ls
from sagas.nlu.anal import build_anal_tree, Doc, AnalNode
from sagas.modules.life.data_source import engine, restaurant, hotel, metadata
from sagas.nlu.anal_expr import match
from sagas.nlu.anal_data_types import behave_, desc_, phrase_, rel_, path_, _
import pandas as pd
import json
from pprint import pprint
from sagas.conf.conf import cf
import sagas.tracker_fn as tc

class restaurant_agent(agent_base):
    def browse(self, pred):
        table_name = self.ds.name
        query = f"select * from {table_name} limit 2"
        df = pd.read_sql_query(query, engine)
        return json.loads(df.to_json(orient='records'))

    def __call__(self, f):
        r = match(f,
                  behave_(_, 'quote|引用', _, _), self.browse,
                  behave_(_, 'perception|感知', _, _), lambda arg: 'perception',
                  behave_(_, 'perception|感知', desc_('result|结果', _), _), lambda arg: arg.text,
                  _, None
                  )
        return r


class hotel_agent(agent_base):
    def __call__(self, f):
        print(f.text)
        return f.text


registry_meta_ls([ds_meta(restaurant_agent(restaurant),
                          ['InstitutePlace|场所',
                           'location: eat|吃',
                           'domain: commerce|商业'
                           ]),
                  ds_meta(hotel_agent(hotel),
                          ['InstitutePlace|场所',
                           'location: eat|吃',
                           'location: reside|住下',
                           'domain: commerce|商业'
                           ]),
                  ])

class Agents(object):
    def do(self, sents, lang='en'):
        """
        $ python -m sagas.modules.life.agents do 'list some restaurants' en
        :param sents:
        :param lang:
        :return:
        """
        f = build_anal_tree(sents, lang, cf.engine(lang))
        tc.emp('cyan', '❏', f.doc.sents)
        f.draw()
        target = f.model().target
        tc.emp('red', '☞', target.text, target.types)

        for m in global_meta_ls():
            print('-' * 25)

            rset = [(cond, target.match(cond)) for cond in m.cond]
            succ = all([r for c, r in rset])
            tc.emp('green' if succ else 'white', '✔' if succ else '✘',
                   m.agent.ds.name, rset)
            if succ:
                r = m.agent(f)
                if r:
                    pprint(r)
                else:
                    print('result -> _')

if __name__ == '__main__':
    import fire
    fire.Fire(Agents)

