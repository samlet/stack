from typing import Text, Any, Dict, List, Union
import datetime
from mongoengine import *

connect('sagas')

class BasePost(Document):
    lang = StringField(required=True, max_length=200)
    posted = DateTimeField(default=datetime.datetime.utcnow)
    tags = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True}

class SentsPost(BasePost):
    content = StringField(required=True)


def post_sents(sents:Text, lang:Text, tags:List[Text]):
    post = SentsPost(lang=lang, content=sents)
    post.tags = tags
    post.save()

class PostsCli(object):
    def query_sents(self):
        """
        # $ sj '牛乳を流しに注いだ。'
            pat(5, name='predict_pour').verb(tags('pour_liquid'), specsof('*', 'pour'),
                                             ヲ=kindof('liquid', 'n'),
                                             ニ=kindof('kitchen_sink', '*')),
        $ python -m sagas.nlu.sinker_orm query_sents
        :return:
        """
        for post in BasePost.objects:
            print('===', post.lang, '===')
            if isinstance(post, SentsPost):
                print(post.content)

    def count_tag(self, tag):
        """
        $ python -m sagas.nlu.sinker_orm count_tag pour_liquid
        :param tag:
        :return:
        """
        return BasePost.objects(tags=tag).count()

if __name__ == '__main__':
    import fire
    fire.Fire(PostsCli)

