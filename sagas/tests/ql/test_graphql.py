"""
$ pytest -s -v test_graphql.py
"""
from graphql import graphql_sync
from ariadne import make_executable_schema, load_schema_from_path, ObjectType, QueryType
from pprint import pprint

import json

def building_with_id(_, info, _id):
    with open('./buildings.json') as file:
        data = json.load(file)
        for building in data['buildings']:
            if building['id'] == _id:
                return building

def resolve_residents_in_building(building, info):
    print(building)
    with open('./residents.json') as file:
        data = json.load(file)
        residents = [
            resident
            for resident
            in data['residents']
            if resident['building']
            == building['id']]
        return residents

def test_graphql():
    type_defs = load_schema_from_path('schema.graphql')

    query = QueryType()
    building = ObjectType('Building')
    resident = ObjectType('Resident')

    # test dataset
    rec = building_with_id(None, None, "1")
    assert rec=={'id': '1', 'buildYear': 2009}
    residents=resolve_residents_in_building(rec, None)
    assert len(residents)>0

    # field holders
    query.set_field('building_with_id', building_with_id)
    building.set_field('residents', resolve_residents_in_building)

    schema = make_executable_schema(type_defs, [building, resident, query])

    q = """{
        building_with_id(_id:"1"){
            id
            residents {
                id
                name
            }
        }
    }
    """
    result = graphql_sync(schema, q)
    pprint(result.data)
    assert result.data['building_with_id']['id']=='1'

