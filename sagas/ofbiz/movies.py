import json
import graphene
from sagas.ofbiz.schema_queries_g import *
from sagas.ofbiz.schema_mutations_g import Mutations

from py4j.java_gateway import java_import
from sagas.ofbiz.runtime_context import platform

oc = platform.oc
finder = platform.finder
helper = platform.helper

java_import(oc.j, 'org.apache.ofbiz.entity.util.*')


class Query(graphene.ObjectType):
    movies = graphene.List(lambda: SaMovie, limit=graphene.Int(),
                           offset=graphene.Int())
    movie_genres = graphene.List(lambda: SaMovieGenres)

    def resolve_movies(self, info, limit=None, offset=None, **kwargs):
        entity_name = "SaMovie"
        # recs = oc.all(entity_name)
        # print("total record", len(recs))
        findOptions = oc.j.EntityFindOptions()
        if limit is None:
            limit = 5
        if offset is None:
            offset = 0

        # print(limit, offset)
        findOptions.setLimit(limit)
        findOptions.setOffset(offset)
        recs = oc.delegator.findList("SaMovie", None, None, None, findOptions, False)

        ent = oc.delegator.getModelEntity(entity_name)
        result = helper.fill_records(ent, SaMovie, recs)
        return result

    def resolve_movie_genres(self, info):
        entity_name = "SaMovieGenres"
        recs = oc.all(entity_name)
        ent = oc.delegator.getModelEntity(entity_name)
        result = helper.fill_records(ent, SaMovieGenres, recs)
        return result


schema = graphene.Schema(query=Query, mutation=Mutations)

