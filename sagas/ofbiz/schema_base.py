import graphene

class ModelBase(graphene.ObjectType):
    def __init__(self, helper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper=helper
