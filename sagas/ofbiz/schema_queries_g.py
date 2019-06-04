import graphene
from sagas.ofbiz.util import ModelBase


class Testing(ModelBase):
    last_updated_stamp = graphene.String()
    comments = graphene.String()
    created_tx_stamp = graphene.String()
    testing_type_id = graphene.String()
    testing_size = graphene.Int()
    created_stamp = graphene.String()
    testing_id = graphene.String()
    description = graphene.String()
    last_updated_tx_stamp = graphene.String()
    testing_date = graphene.String()
    testing_name = graphene.String()
    testing_type = graphene.Field(lambda: TestingType)
    testing_item = graphene.List(lambda: TestingItem)
    testing_node_member = graphene.List(lambda: TestingNodeMember)

    def resolve_testing_type(self, info):
        return self.helper.get_related_one("TestingType", TestingType, testingTypeId=self.testing_type_id)

    def resolve_testing_item(self, info):
        return self.helper.get_relations("TestingItem", TestingItem, testingId=self.testing_id)

    def resolve_testing_node_member(self, info):
        return self.helper.get_relations("TestingNodeMember", TestingNodeMember, testingId=self.testing_id)

class TestingType(ModelBase):
    last_updated_stamp = graphene.String()
    created_tx_stamp = graphene.String()
    testing_type_id = graphene.String()
    created_stamp = graphene.String()
    description = graphene.String()
    last_updated_tx_stamp = graphene.String()
    testing = graphene.List(lambda: Testing)

    def resolve_testing(self, info):
        return self.helper.get_relations("Testing", Testing, testingTypeId=self.testing_type_id)

class TestingItem(ModelBase):
    last_updated_stamp = graphene.String()
    testing_history = graphene.String()
    created_tx_stamp = graphene.String()
    created_stamp = graphene.String()
    testing_id = graphene.String()
    last_updated_tx_stamp = graphene.String()
    testing_seq_id = graphene.String()
    testing = graphene.Field(lambda: Testing)

    def resolve_testing(self, info):
        return self.helper.get_related_one("Testing", Testing, testingId=self.testing_id)

class TestingNode(ModelBase):
    last_updated_stamp = graphene.String()
    created_tx_stamp = graphene.String()
    created_stamp = graphene.String()
    description = graphene.String()
    last_updated_tx_stamp = graphene.String()
    testing_node_id = graphene.String()
    primary_parent_node_id = graphene.String()
    primary_parent_testing_node = graphene.Field(lambda: TestingNode)
    primary_child_testing_node = graphene.List(lambda: TestingNode)
    testing_node_member = graphene.List(lambda: TestingNodeMember)

    def resolve_primary_parent_testing_node(self, info):
        return self.helper.get_related_one("TestingNode", TestingNode, testingNodeId=self.primary_parent_node_id)

    def resolve_primary_child_testing_node(self, info):
        return self.helper.get_relations("TestingNode", TestingNode, primaryParentNodeId=self.testing_node_id)

    def resolve_testing_node_member(self, info):
        return self.helper.get_relations("TestingNodeMember", TestingNodeMember, testingNodeId=self.testing_node_id)

class TestingNodeMember(ModelBase):
    from_date = graphene.String()
    last_updated_stamp = graphene.String()
    extend_from_date = graphene.String()
    created_tx_stamp = graphene.String()
    created_stamp = graphene.String()
    testing_id = graphene.String()
    last_updated_tx_stamp = graphene.String()
    extend_thru_date = graphene.String()
    testing_node_id = graphene.String()
    thru_date = graphene.String()
    testing = graphene.Field(lambda: Testing)
    testing_node = graphene.Field(lambda: TestingNode)

    def resolve_testing(self, info):
        return self.helper.get_related_one("Testing", Testing, testingId=self.testing_id)

    def resolve_testing_node(self, info):
        return self.helper.get_related_one("TestingNode", TestingNode, testingNodeId=self.testing_node_id)

class SaMovie(ModelBase):
    overview = graphene.String()
    last_updated_stamp = graphene.String()
    vote_average = graphene.Float()
    release_date = graphene.String()
    created_tx_stamp = graphene.String()
    created_stamp = graphene.String()
    last_updated_tx_stamp = graphene.String()
    movie_id = graphene.String()
    video = graphene.String()
    title = graphene.String()
    original_language = graphene.String()
    original_title = graphene.String()
    popularity = graphene.Float()
    vote_count = graphene.Int()
    backdrop_path = graphene.String()
    poster_path = graphene.String()
    sa_movie_genres_appl = graphene.List(lambda: SaMovieGenresAppl)

    def resolve_sa_movie_genres_appl(self, info):
        return self.helper.get_relations("SaMovieGenresAppl", SaMovieGenresAppl, movieId=self.movie_id)

class SaMovieGenres(ModelBase):
    movie_genres_name = graphene.String()
    last_updated_stamp = graphene.String()
    movie_genres_id = graphene.String()
    created_tx_stamp = graphene.String()
    created_stamp = graphene.String()
    last_updated_tx_stamp = graphene.String()
    sa_movie_genres_appl = graphene.List(lambda: SaMovieGenresAppl)

    def resolve_sa_movie_genres_appl(self, info):
        return self.helper.get_relations("SaMovieGenresAppl", SaMovieGenresAppl, movieGenresId=self.movie_genres_id)

class SaMovieGenresAppl(ModelBase):
    last_updated_stamp = graphene.String()
    movie_genres_id = graphene.String()
    created_tx_stamp = graphene.String()
    created_stamp = graphene.String()
    last_updated_tx_stamp = graphene.String()
    movie_id = graphene.String()
    sa_movie = graphene.Field(lambda: SaMovie)
    sa_movie_genres = graphene.Field(lambda: SaMovieGenres)

    def resolve_sa_movie(self, info):
        return self.helper.get_related_one("SaMovie", SaMovie, movieId=self.movie_id)

    def resolve_sa_movie_genres(self, info):
        return self.helper.get_related_one("SaMovieGenres", SaMovieGenres, movieGenresId=self.movie_genres_id)
