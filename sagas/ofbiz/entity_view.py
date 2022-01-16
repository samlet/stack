from typing import Text, Any, Dict, List, Union, Optional
import sagas.ofbiz.entities as ee
from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class ViewEntity:
    name: str
    title: str
    description: str
    pkg: str
    members: List[Dict]
    links: List[Dict]
    aliases: List[Dict]
    rels: List[Dict]


def view_info(ent: ee.MetaEntity) -> ViewEntity:
    members = ent.model.getAllModelMemberEntities()

    links = ent.model.getViewLinksCopy()
    aliases = ent.model.getAliasesCopy()
    rels = ent.model.getRelations()

    return ViewEntity(name=ent.name, title=ent.model.getTitle(),
                      description=ent.model.getDescription(),
                      pkg=ent.model.getPackageName(),
                      members=[{'ent': ent.getEntityName(), 'alias': ent.getEntityAlias()} for ent in members],
                      links=[{'ent': link.getEntityAlias(),
                              'rel': link.getRelEntityAlias(),
                              'keymaps': [{ks.getFieldName(): ks.getRelFieldName()} for ks in link.getKeyMapsCopy()],
                              } for link in links],
                      aliases=[{'name': a.getName(),
                                'field': a.getField(),
                                'entity_alias': a.getEntityAlias(),
                                'col_alias': a.getColAlias(),
                                'description': a.getDescription(),
                                'group_by': a.getGroupBy(),
                                'function': a.getFunction(),
                                'field_set': a.getFieldSet(),
                                } for a in aliases],
                      rels=[{'name': rel.getCombinedName(),
                             'title': rel.getTitle(),
                             'rel_entity_name': rel.getRelEntityName(),
                             'type': rel.getType(),
                             'fkName': rel.getFkName(),
                             'keymaps': [{'field_name': ks.getFieldName(),
                                          'rel_field_name': ks.getRelFieldName()} for ks in rel.getKeyMaps()],
                             } for rel in rels]
                      )


def get_views(vals: List[str]):
    return [view_info(ee.entity(v)).to_dict() for v in vals if ee.entity(v).is_view()]
