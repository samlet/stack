from __future__ import absolute_import

import enum

from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy.registry import get_global_registry
from sagas.misc.utils import to_std_dicts
from sqlalchemy import (Column, Date, Enum, ForeignKey, Integer, String, Table,
                        func, select)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, composite, mapper, relationship
import graphene
from graphene.relay import Connection, Node

PetKind = Enum("cat", "dog", name="pet_kind")

class HairKind(enum.Enum):
    LONG = 'long'
    SHORT = 'short'


Base = declarative_base()

association_table = Table(
    "association",
    Base.metadata,
    Column("pet_id", Integer, ForeignKey("pets.id")),
    Column("reporter_id", Integer, ForeignKey("reporters.id")),
)


class Editor(Base):
    __tablename__ = "editors"
    editor_id = Column(Integer(), primary_key=True)
    name = Column(String(100))


class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer(), primary_key=True)
    name = Column(String(30))
    pet_kind = Column(PetKind, nullable=False)
    hair_kind = Column(Enum(HairKind, name="hair_kind"), nullable=False)
    reporter_id = Column(Integer(), ForeignKey("reporters.id"))


class CompositeFullName(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __composite_values__(self):
        return self.first_name, self.last_name

    def __repr__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Reporter(Base):
    __tablename__ = "reporters"

    id = Column(Integer(), primary_key=True)
    first_name = Column(String(30), doc="First name")
    last_name = Column(String(30), doc="Last name")
    email = Column(String(), doc="Email")
    favorite_pet_kind = Column(PetKind)
    pets = relationship("Pet", secondary=association_table, backref="reporters")
    articles = relationship("Article", backref="reporter")
    favorite_article = relationship("Article", uselist=False)

    @hybrid_property
    def hybrid_prop(self):
        return self.first_name

    column_prop = column_property(
        select([func.cast(func.count(id), Integer)]), doc="Column property"
    )

    composite_prop = composite(CompositeFullName, first_name, last_name, doc="Composite")


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer(), primary_key=True)
    headline = Column(String(100))
    pub_date = Column(Date())
    reporter_id = Column(Integer(), ForeignKey("reporters.id"))


class ReflectedEditor(type):
    """Same as Editor, but using reflected table."""

    @classmethod
    def __subclasses__(cls):
        return []


editor_table = Table("editors", Base.metadata, autoload=True)

mapper(ReflectedEditor, editor_table)

############################

def add_test_data(session):
    reporter = Reporter(
        first_name='John', last_name='Doe', favorite_pet_kind='cat')
    session.add(reporter)
    pet = Pet(name='Garfield', pet_kind='cat', hair_kind=HairKind.SHORT)
    session.add(pet)
    pet.reporters.append(reporter)
    article = Article(headline='Hi!')
    article.reporter = reporter
    session.add(article)
    reporter = Reporter(
        first_name='Jane', last_name='Roe', favorite_pet_kind='dog')
    session.add(reporter)
    pet = Pet(name='Lassie', pet_kind='dog', hair_kind=HairKind.LONG)
    pet.reporters.append(reporter)
    session.add(pet)
    editor = Editor(name="Jack")
    session.add(editor)
    session.commit()

def convert_sqlalchemy_composite(composite_prop, registry, resolver):
    converter = registry.get_converter_for_composite(composite_prop.composite_class)
    if not converter:
        try:
            raise Exception(
                "Don't know how to convert the composite field %s (%s)"
                % (composite_prop, composite_prop.composite_class)
            )
        except AttributeError:
            # handle fields that are not attached to a class yet (don't have a parent)
            raise Exception(
                "Don't know how to convert the composite field %r (%s)"
                % (composite_prop, composite_prop.composite_class)
            )

    # TODO Add a way to override composite fields default parameters
    return converter(composite_prop, registry)

def _register_composite_class(cls, registry=None):
    if registry is None:
        # from .registry import get_global_registry

        registry = get_global_registry()

    def inner(fn):
        registry.register_composite_converter(cls, fn)

    return inner


convert_sqlalchemy_composite.register = _register_composite_class

def test_query_fields(session):
    add_test_data(session)

    @convert_sqlalchemy_composite.register(CompositeFullName)
    def convert_composite_class(composite, registry):
        return graphene.String()

    class ReporterType(SQLAlchemyObjectType):
        class Meta:
            model = Reporter

    class Query(graphene.ObjectType):
        reporter = graphene.Field(ReporterType)
        reporters = graphene.List(ReporterType)

        def resolve_reporter(self, _info):
            return session.query(Reporter).first()

        def resolve_reporters(self, _info):
            return session.query(Reporter)

    query = """
        query {
          reporter {
            firstName
            columnProp
            hybridProp
            compositeProp
          }
          reporters {
            firstName
          }
        }
    """
    # expected = {
    #     "reporter": {
    #         "firstName": "John",
    #         "hybridProp": "John",
    #         "columnProp": 2,
    #         "compositeProp": "John Doe",
    #     },
    #     "reporters": [{"firstName": "John"}, {"firstName": "Jane"}],
    # }
    schema = graphene.Schema(query=Query)
    result = schema.execute(query)
    assert not result.errors
    result = to_std_dicts(result.data)
    return result

class ScenarioReporter(object):
    def __init__(self, recreate=True):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import scoped_session, sessionmaker

        # db = create_engine(test_db_url)
        db = create_engine('sqlite:///out/scenario_reporter.db', convert_unicode=True)
        connection = db.engine.connect()
        transaction = connection.begin()

        if recreate:
            Base.metadata.drop_all(connection)  # drop all exists tables
            Base.metadata.create_all(connection)

        # options = dict(bind=connection, binds={})
        session_factory = sessionmaker(bind=connection)
        self.session = scoped_session(session_factory)

    def query(self):
        """
        $ python -m sagas.feedback_loop.scenario_reporter query
        :return:
        """
        from pprint import pprint
        r=test_query_fields(self.session)
        pprint(r)

sc_reporter= ScenarioReporter(recreate=False)

if __name__ == '__main__':
    import fire
    fire.Fire(ScenarioReporter)

