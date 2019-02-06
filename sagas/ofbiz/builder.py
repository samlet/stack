from tabulate import tabulate
from sagas.util.str_converters import to_camel_case, to_snake_case
from sagas.util.string_util import abbrev
import fire

from sagas.ofbiz.runtime_context import platform

oc=platform.oc
finder=platform.finder

# oc=OfbizConnector()
# finder=Finder(oc)

def desc_relations(entity_name):
    table_header = ['name','type', 'string']
    table_data = []
    ent=oc.delegator.getModelEntity(entity_name)
    # print(ent.getPlainTableName(), ent.getTitle(), ent.getDescription())
    for rel in ent.getRelationsList(True, True, True):
        # print("\t", rel.getType(), rel)
        table_data.append((abbrev(rel.getRelEntityName(), 20),
                        rel.getType(),
                        abbrev(rel.getTitle()+rel.getRelEntityName(), 25)))
    print(tabulate(table_data, headers=table_header, tablefmt='psql'))

def desc_model(entity_name, include_auto_fields=True):
    ent = oc.delegator.getModelEntity(entity_name)
    print(ent.getPlainTableName(), ent.getTitle(), ent.getDescription())
    table_header = ['name', 'type', 'string']
    table_data = []
    names = ent.getAllFieldNames()
    autoflds = ent.getAutomaticFieldNames()
    for field_name in names:
        if (not include_auto_fields) and (field_name in autoflds):
            pass
        else:
            fld = ent.getField(field_name)
            table_data.append((abbrev(field_name, 20),
                               fld.getType(),
                               abbrev(fld.getColName(), 25)))
    print(tabulate(table_data, headers=table_header, tablefmt='psql'))
    desc_relations(entity_name)

# the date and time types:
#     <field-type-def type="date-time" sql-type="DATETIME(3)" java-type="java.sql.Timestamp"/>
#     <field-type-def type="date" sql-type="DATE" java-type="java.sql.Date"/>
#     <field-type-def type="time" sql-type="TIME(3)" java-type="java.sql.Time"/>
type_mappings={"string":["blob","byte-array","object",
                         "date-time","date","time",
                         "id","id-long","id-vlong",
                        "indicator","very-short","short-varchar","long-varchar","very-long",
                        "comment","description","name","value",
                        "credit-card-number","credit-card-date","email","url","tel-number"],
              "float":["currency-amount","currency-precise","fixed-point","floating-point"],
              "int":["numeric"]}
gl_mappings={"string":"String", "float":"Float", "int":"Int"}

def get_mapping_type(field_type):
    for k, v in type_mappings.items():
        if field_type in v:
            return k
    raise ValueError("Cannot find mapping type for "+field_type)

def get_graphql_type(field_type):
    mt=get_mapping_type(field_type)
    return gl_mappings[mt]

program_header='''import graphene
from sagas.ofbiz.util import ModelBase
'''
program_footer='''
schema = graphene.Schema(query=Query)
'''
resover_def='''
    def resolve_{rel_name}(self, info):
        return self.helper.{method}("{model}", {model}, {inputs})'''

def gen_model_class():
    headers = []
    footers = []
    headers.append(program_header)
    footers.append(program_footer)

    def gen_model(entity_name):
        lines = []
        resolvers = []
        ent = oc.delegator.getModelEntity(entity_name)

        lines.append("class {ent}(ModelBase):".format(ent=entity_name))
        names = ent.getAllFieldNames()
        for field_name in names:
            fld = ent.getField(field_name)
            fldtype = get_graphql_type(fld.getType())
            lines.append("    {name} = graphene.{type}()".format(name=to_snake_case(field_name),
                                                                 type=fldtype))

        for rel in ent.getRelationsList(True, False, True):
            model_name = rel.getRelEntityName()
            # relation_name = rel.getTitle() + rel.getRelEntityName()
            rel_name = to_snake_case(rel.getTitle()+model_name)
            # extract relation fields
            inputs = []
            for key in rel.getKeyMaps():
                inputs.append("{}=self.{}".format(key.getRelFieldName(),
                                                  to_snake_case(key.getFieldName())))
            # build
            if rel.getType() == "many":
                method = "get_relations"
                lines.append("    {name} = graphene.List(lambda: {model})".format(
                    name=rel_name, model=model_name))
            else:
                method = "get_related_one"
                lines.append("    {name} = graphene.Field(lambda: {model})".format(
                    name=rel_name, model=model_name))
            resolvers.append(resover_def.format(rel_name=rel_name,
                                                model=model_name,
                                                method=method,
                                                inputs=", ".join(inputs)))
        return "\n".join(lines + resolvers)

    all_models = []
    models = ["Testing", "TestingType", "TestingItem",
              "TestingNode", "TestingNodeMember",
              "SaMovie", "SaMovieGenres", "SaMovieGenresAppl"
              ]
    for mo in models:
        all_models.append(gen_model(mo))
    # program=("\n".join(headers+lines+resolvers+footers))
    program = ("\n\n".join(headers + all_models))
    print(program)

class Builder(object):
    def __init__(self):
        pass

    def desc_model(self, entity):
        desc_model(entity)

    def gen_model(self):
        gen_model_class()

if __name__ == '__main__':
    fire.Fire(Builder)
