class OperValue(object):
    def __init__(self, vtype=None, left=None, op=None, right=None, alias=None):
        self.alias = alias
        self._type = vtype
        self._left = left
        self._op = op
        self._right = right

    def __lt__(self, other):
        return OperValue(self._type, self._left, '$lt', other, self.alias)

    def __floordiv__(self, other):
        return OperValue(self._type, self, '$sub', other, self.alias)

    def __rshift__(self, other):
        return OperValue(self._type, self, '$for', other, self.alias)

    def __call__(self, *args):
        return OperValue(self._type, self._left, op='predicate', right=args, alias=self.alias)


class Closure(object):
    def __getattr__(self, name):
        # print(f'...... closure {name}')
        return OperValue(name)


ud = Closure()


