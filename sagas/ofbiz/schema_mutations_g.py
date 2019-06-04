import graphene
from sagas.ofbiz.util import ModelBase
from sagas.ofbiz.schema_queries_g import *
from sagas.ofbiz.runtime_context import platform

class TestingTypeInput(graphene.InputObjectType):
    testing_type_id = graphene.String()
    description = graphene.String()

class CreateTestingType(graphene.Mutation):
    class Arguments:
        testing_type_data = TestingTypeInput(required=True)

    testing_type = graphene.Field(lambda: TestingType)
    Output = TestingType

    @staticmethod
    def mutate(root, info, testing_type_data=None):
        testing_type = platform.helper.input_to_dictionary(testing_type_data, "TestingType", TestingType)        
        return testing_type

class TestingInput(graphene.InputObjectType):
    comments = graphene.String()
    testing_type_id = graphene.String()
    testing_size = graphene.Int()
    testing_id = graphene.String()
    description = graphene.String()
    testing_date = graphene.String()
    testing_name = graphene.String()

class CreateTesting(graphene.Mutation):
    class Arguments:
        testing_data = TestingInput(required=True)

    testing = graphene.Field(lambda: Testing)
    Output = Testing

    @staticmethod
    def mutate(root, info, testing_data=None):
        testing = platform.helper.input_to_dictionary(testing_data, "Testing", Testing)        
        return testing

class Mutations(graphene.ObjectType):
    create_testing_type = CreateTestingType.Field()
    create_testing = CreateTesting.Field()
