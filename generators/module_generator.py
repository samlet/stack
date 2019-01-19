#!/usr/bin/env python
import io
import os
import shutil
from shutil import copyfile

import yaml
import sys
import fire

sys.path.append("..")
from sagas.util.str_converters import to_camel_case
import io_utils

def is_true(node, attr):
    return (attr in node) and node[attr]
def is_primary(node):
    return is_true(node, "primary")

class ModelDefinitions(object):
    def __init__(self, file_name):
        self.models={}
        self.base_models={}
        with open(file_name) as f:
            # use safe_load instead load
            self.doc_root = yaml.safe_load(f)
            self.name=self.doc_root["name"]
            self.models_root=self.doc_root['models']
            self.database_root=self.doc_root['database']
            for k, model in self.models_root.items():
                # print(k, model['name'])
                if is_true(model, 'abstract'):
                    # print("\tabstract", model['abstract'])
                    self.base_models[k]=model
                    pass
                else:
                    self.models[k]=model

# model_def=ModelDefinitions('model_planet.yaml')

model_header='''## autogenerate
from .base import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Model{cname}(Base):
    """{cname} model."""

    __tablename__ = '{name}'
'''

def gen_model_header(model_def, model_name):
    # model_name='people'
    # model_name='planet'
    return(model_header.format(name=model_name,
                              cname=to_camel_case(model_name, True),
                              model=model_def.models[model_name]))

field_def='''{fld_name} = Column('{fld_name}', {fld_type}, {pk_part}{fk_part} doc="{field[doc]}")'''
rel_def='''{lname} = relationship(Model{model}, backref='{field[backref]}')'''
rel_imp_def="from .model_{model} import Model{cmodel}"
def gen_model_fields(model_def, model_name):
    field_builder = []
    imports_builder=[]
    import_set=[]
    model=model_def.models[model_name]
    for k, fld in model['fields'].items():
        primary_part = ""
        foreign_part=""
        if is_primary(fld):
            primary_part = "primary_key=True,"
        if "foreign_key" in fld:
            foreign_part="ForeignKey('{}'),".format(fld['foreign_key'])
        if fld['type'] == "relation":
            rel_model=fld['model']
            field_builder.append(rel_def.format(
                lname=to_camel_case(k),
                model=to_camel_case(rel_model, True),
                field=fld
            ))
            if rel_model not in import_set:
                import_set.append(rel_model)
                imports_builder.append(rel_imp_def.format(model=rel_model,
                                                          cmodel=to_camel_case(rel_model, True)))
        else:
            # print(fld['doc'])
            field_builder.append(field_def.format(fld_name=k,
                                                  fld_type=fld['type'].capitalize(),
                                                  pk_part=primary_part,
                                                  fk_part=foreign_part,
                                                  field=fld))

    # process extends
    if 'extends' in model:
        base_model = model_def.base_models[model['extends']]
        for k, fld in base_model['fields'].items():
            # print(k)
            field_builder.append(field_def.format(fld_name=k,
                                                  fld_type=fld['type'].capitalize(),
                                                  pk_part="",
                                                  fk_part="",
                                                  field=fld))
    return("    " + "\n    ".join(imports_builder+field_builder))

schema_header='''from datetime import datetime
from graphene_sqlalchemy import SQLAlchemyObjectType
from database.base import db_session
from database.model_{name} import Model{cname}
import graphene
import utils


# Create a generic class to mutualize description of {name} attributes for both queries and mutations
class {cname}Attribute:
'''
def gen_schema_header(model_def, model_name):
    return (schema_header.format(name=model_name,
                               cname=to_camel_case(model_name, True),
                               model=model_def.models[model_name]))

type_map={"string":"String", "integer":"Int"}

def is_input(node):
    if 'input' in node:
        return node['input']
    return True
def get_graphql_type(fld_name, fld_type):
    if fld_name.endswith('_id'):
        return "ID"
    return type_map[fld_type]

def gen_schema_fields(model_def, model_name):
    field_def = '''{fld_name} = graphene.{fld_type}(description="{field[doc]}")'''
    field_builder = []
    model=model_def.models[model_name]
    for k, fld in model['fields'].items():
        if fld['type'] == "relation":
            pass
        elif is_input(fld):
            field_builder.append(field_def.format(fld_name=k,
                                                  fld_type=get_graphql_type(k, fld['type']),
                                                  field=fld))
    # process extends
    if 'extends' in model:
        base_model = model_def.base_models[model['extends']]
        for k, fld in base_model['fields'].items():
            if is_input(fld):
                field_builder.append(field_def.format(fld_name=k,
                                                  fld_type=get_graphql_type(k, fld['type']),
                                                  field=fld))
    return ("    " + "\n    ".join(field_builder))

creator_def='''
class {model[name]}(SQLAlchemyObjectType):
    """{model[name]} node."""

    class Meta:
        model = Model{model[name]}
        interfaces = (graphene.relay.Node,)

###
class Create{model[name]}Input(graphene.InputObjectType, {model[name]}Attribute):
    """Arguments to create a {name}."""
    pass


class Create{model[name]}(graphene.Mutation):
    """Mutation to create a {name}."""
    {name} = graphene.Field(lambda: {model[name]}, description="{model[name]} created by this mutation.")

    class Arguments:
        input = Create{model[name]}Input(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        data['created'] = str(datetime.utcnow())
        data['edited'] = str(datetime.utcnow())

        {name} = Model{model[name]}(**data)
        db_session.add({name})
        db_session.commit()

        return Create{model[name]}({name}={name})
'''

def gen_schema_creator(model_def, model_name):
    return (creator_def.format(name=model_name,
                             cname=to_camel_case(model_name, True),
                             model=model_def.models[model_name]))

updater_def='''
class Update{model[name]}Input(graphene.InputObjectType, {model[name]}Attribute):
    """Arguments to update a {name}."""
    id = graphene.ID(required=True, description="Global Id of the {name}.")


class Update{model[name]}(graphene.Mutation):
    """Update a {name}."""
    {name} = graphene.Field(lambda: {model[name]}, description="{model[name]} updated by this mutation.")

    class Arguments:
        input = Update{model[name]}Input(required=True)

    def mutate(self, info, input):
        data = utils.input_to_dictionary(input)
        data['edited'] = str(datetime.utcnow())

        {name} = db_session.query(Model{model[name]}).filter_by(id=data['id'])
        {name}.update(data)
        db_session.commit()
        {name} = db_session.query(Model{model[name]}).filter_by(id=data['id']).first()

        return Update{model[name]}({name}={name})
'''
def gen_schema_updater(model_def, model_name):
    return (updater_def.format(name=model_name,
                             cname=to_camel_case(model_name, True),
                             model=model_def.models[model_name]))

def gen_schema_file(model_def):
    lines = []
    lines.append('from graphene_sqlalchemy import SQLAlchemyConnectionField')
    lines.append('import graphene')
    for mo in model_def.models:
        lines.append("import schema_{}".format(mo))

    ## queries
    lines.append('''
class Query(graphene.ObjectType):
    """Nodes which can be queried by this API."""
    node = graphene.relay.Node.Field()''')
    for mo in model_def.models:
        lines.append('''    # {cname}
    {name} = graphene.relay.Node.Field(schema_{name}.{cname})
    {name}List = SQLAlchemyConnectionField(schema_{name}.{cname})'''.format(
            name=mo, cname=mo.capitalize()))
    ## mutations
    lines.append('''
class Mutation(graphene.ObjectType):
    """Mutations which can be performed by this API."""''')
    for mo in model_def.models:
        lines.append('''    # {cname} mutation
    create{cname} = schema_{name}.Create{cname}.Field()
    update{cname} = schema_{name}.Update{cname}.Field()'''.format(
            name=mo, cname=mo.capitalize()))

    lines.append("schema = graphene.Schema(query=Query, mutation=Mutation)")
    return ("\n".join(lines))

def gen_setup_file(model_def):
    lines = []
    lines.append('''from ast import literal_eval
from database import base
import logging
import sys''')
    for mo in model_def.models:
        lines.append("from database.model_{} import Model{}".format(mo, mo.capitalize()))
    lines.append('''
# Load logging configuration
log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == '__main__':
    #+ remove all tables
    base.Base.metadata.drop_all(base.engine)

    log.info('Create database {}'.format(base.db_name))
    base.Base.metadata.create_all(base.engine)''')
    for mo in model_def.models:
        lines.append('''    log.info('Insert {cname} data in database')
    with open('database/data/{name}.json', 'r') as file:
        data = literal_eval(file.read())
        for record in data:
            {name} = Model{cname}(**record)
            base.db_session.add({name})
        base.db_session.commit()'''.format(
            name=mo, cname=mo.capitalize()))

    return ("\n".join(lines))

def write_model(model_def, model_name):
    prefix="output/"+model_def.name
    filename="{}/database/model_{}.py".format(prefix, model_name)
    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(gen_model_header(model_def, model_name))
        f.write(gen_model_fields(model_def, model_name))

    filename = "{}/schema_{}.py".format(prefix, model_name)
    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(gen_schema_header(model_def, model_name))
        f.write(gen_schema_fields(model_def, model_name))
        f.write(gen_schema_creator(model_def, model_name))
        f.write(gen_schema_updater(model_def, model_name))

    filename = "{}/schema.py".format(prefix)
    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(gen_schema_file(model_def))

    filename = "{}/setup.py".format(prefix)
    with io.open(filename, 'w', encoding="utf-8") as f:
        f.write(gen_setup_file(model_def))

database_def='''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

## Create database engine: cockroach
db_name = '{db[name]}'
connect_args = {db[connect_args]}

engine = create_engine(
    '{db[url]}',
    connect_args=connect_args,
    echo=True                   # Log SQL queries to stdout
)

# Declarative base model to create database tables and classes
Base = declarative_base()
Base.metadata.bind = engine  # Bind engine to metadata of the base class

# Create database session object
db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
Base.query = db_session.query_property()  # Used by graphql to execute queries

'''
def write_db_settings(model_def, target_file):
    # db = model_def.database_root
    with io.open(target_file, 'w', encoding="utf-8") as f:
        f.write(database_def.format(db=model_def.database_root))

def create_model_def(def_file):
    model_def = ModelDefinitions(def_file)
    return model_def

def gen_module(file, recreate):
    model_def = create_model_def(file)
    prefix = "./output/"
    module_name = model_def.name
    module_path = prefix + module_name

    if recreate and os.path.isdir(module_path):
        shutil.rmtree(module_path)

    if os.path.isdir(module_path):
        print("module folder", module_path, "already exists.")
        return

    io_utils.create_dir(module_path)
    db_path = module_path + "/database"
    seed_path = module_path + "/database/data"
    io_utils.create_dir(seed_path)

    copyfile("./templates/api.py", module_path + "/api.py")
    copyfile("./templates/utils.py", module_path + "/utils.py")

    ## copy seed files
    for path in io_utils.list_files("./seeds/" + module_name):
        copyfile(path, seed_path + "/" + os.path.basename(path))

    write_db_settings(model_def, db_path + "/base.py")
    for m in model_def.models:
        write_model(model_def, m)

    print("all done.")

class ModuleGenerator(object):
    def hi(self):
        print("just say hi.")

    def test_people(self, file='model_planet.yaml'):
        model_def=create_model_def(file)
        print(".. getting people fields")
        for k, fld in model_def.models['people']['fields'].items():
            print(k, is_primary(fld), is_true(fld, 'input'))

    def show_db(self, file='model_planet.yaml'):
        model_def = create_model_def(file)
        db=model_def.database_root
        print(db['url'])

    def gen_model(self, file='model_planet.yaml'):
        model_def = create_model_def(file)
        write_model(model_def, "people")

    def regen_models(self, file='model_planet.yaml'):
        gen_module(file, True)

    def gen_models(self, file='model_planet.yaml'):
        gen_module(file, False)

if __name__ == '__main__':
    fire.Fire(ModuleGenerator)
