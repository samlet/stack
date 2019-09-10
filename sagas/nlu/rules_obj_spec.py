from sagas.nlu.aiobj_base import BaseMeta, Keeper
from sagas.nlu.inspectors import NegativeWordInspector as negative
from sagas.nlu.inspectors import DateInspector as dateins
from sagas.nlu.inspectors import EntityInspector as entins
from sagas.nlu.inspector_wordnet import PredicateWordInspector as kindof
from sagas.nlu.inspector_wordnet import VerbInspector as behaveof
from sagas.nlu.inspector_rasa import RasaInspector as intentof
from sagas.nlu.patterns import Patterns
from sagas.nlu.ruleset import RuleSet, actions_vob
from sagas.tool.misc import color_print


class StoremanMeta(BaseMeta):
    def __init__(cls, clsname, superclasses, attributedict):
        ruleset_stats = RuleSet('how_many_artifact_c',
                                rules=lambda d, m: [
                                    # $ sz '你有几台笔记本电脑？'
                                    Patterns(d, m, 5).verb(behaveof('have', 'v'), __engine='ltp',
                                                           vob=intentof('how_many', 0.75)),
                                    *actions_vob(d, m, [('have', 'device/artifact'), ]),
                                ],
                                executor=lambda obj: color_print('red', f'.. object: {obj}'))
        cls.rulesets = [ruleset_stats]
        BaseMeta.setup(cls)


class Storeman(Keeper, metaclass=StoremanMeta):
    def __init__(self, name):
        self.name = name

    def callback(self, t):
        print(f'** {self.name} callback', t)
        return self

    def __repr__(self):
        return f"♡{self.name}♡"

class AiObjects(object):
    def storeman(self, sents, lang='zh'):
        """
        $ python -m sagas.nlu.rules_obj_spec storeman '你有几台笔记本电脑？' zh

        >>> from sagas.nlu.rules_obj_spec import Storeman
        >>> a = Storeman("tom")
        >>> b = Storeman("kite")
        >>> a._('你有几台笔记本电脑？', 'zh')
        >>> a._('done.')

        :return:
        """
        a = Storeman("tom")
        b = Storeman("kite")
        # a._('你有几台笔记本电脑？', 'zh')
        a._(sents, lang)

if __name__ == '__main__':
    import fire
    fire.Fire(AiObjects)

