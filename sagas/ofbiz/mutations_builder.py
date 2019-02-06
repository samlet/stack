from sagas.ofbiz.builder import oc, finder, abbrev, get_graphql_type, get_mapping_type
from sagas.util.str_converters import to_camel_case, to_snake_case

creator_def='''
class Create{ctx[model]}(graphene.Mutation):
    class Arguments:
        {ctx[s_model]}_data = {ctx[model]}Input(required=True)

    {ctx[s_model]} = graphene.Field(lambda: {ctx[model]})
    Output = {ctx[model]}

    @staticmethod
    def mutate(root, info, {ctx[s_model]}_data=None):
        {ctx[s_model]} = platform.helper.input_to_dictionary({ctx[s_model]}_data, "{ctx[model]}", {ctx[model]})        
        return {ctx[s_model]}
'''

def gen_model(entity_name, mutations_c):
    gen_ctx = {}
    gen_ctx['model'] = entity_name
    gen_ctx['s_model'] = to_snake_case(entity_name)
    ent = oc.delegator.getModelEntity(entity_name)
    autoflds = ent.getAutomaticFieldNames()

    model_c = []
    model_c.append("class {ctx[model]}Input(graphene.InputObjectType):".format(ctx=gen_ctx))

    names = ent.getAllFieldNames()
    for field_name in names:
        if field_name not in autoflds:
            fld = ent.getField(field_name)
            fldtype = get_graphql_type(fld.getType())
            model_c.append("    {name} = graphene.{type}()".format(name=to_snake_case(field_name),
                                                                   type=fldtype))
    # print("\n".join(model_c))
    model_c.append(creator_def.format(ctx=gen_ctx))
    mutations_c.append("    create_{ctx[s_model]} = Create{ctx[model]}.Field()".format(ctx=gen_ctx))

    print("\n".join(model_c))

program_header='''import graphene
from sagas.ofbiz.util import ModelBase
from sagas.ofbiz.schema_queries_g import *
from sagas.ofbiz.runtime_context import platform
'''

def gen_mutations(entities):

    mutations_c = []
    mutations_c.append("class Mutations(graphene.ObjectType):")

    print(program_header)

    # entity_name = 'TestingType'
    for entity_name in entities:
        gen_model(entity_name, mutations_c)

    print("\n".join(mutations_c))

if __name__ == '__main__':
    entities = ['TestingType', 'Testing']
    gen_mutations(entities)
