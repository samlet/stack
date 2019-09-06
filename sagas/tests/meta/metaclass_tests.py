# https://www.python-course.eu/python3_metaclasses.php
class LittleMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        print("clsname: ", clsname)
        print("superclasses: ", superclasses)
        print("attributedict: ", attributedict)
        return type.__new__(cls, clsname, superclasses, attributedict)

    def __init__(cls, clsname, superclasses, attributedict):
        from sagas.aifuncs.rules_common import ruleset_stats, ruleset_dates
        cls.the_answer = 10
        cls.rulesets = [ruleset_stats, ruleset_dates]

        def _(self, text, lang='en'):
            print(type(self).__name__,
                  isinstance(self, S),
                  text, lang)
            # execute rulesets
            print('rules', [r.name for r in self.rulesets])
            if isinstance(self, S):
                return self.callback(text)
            return None

        cls._ = _

    # def __call__(cls, *args, **kwargs):
    #    print(args, kwargs)


class S:
    def callback(self, t):
        pass

class A(S, metaclass=LittleMeta):
    def __init__(self, name):
        self.name=name

    def callback(self, t):
        print(f'** {self.name} callback', t)
        return self

a = A("tom")
b = A("kite")
print(a.the_answer)
a._('list files', 'en')
a._('done.')
b._('done.').callback('direct')



