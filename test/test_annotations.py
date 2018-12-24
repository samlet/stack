import collections
import functools
import inspect

def foobar(a: int, b: str, c: float = 3.2) -> tuple: pass
def check(func):
    # 获取函数定义的参数
    sig = inspect.signature(func)
    parameters = sig.parameters  # 参数有序字典
    arg_keys = tuple(parameters.keys())  # 参数名称
    for k, v in sig.parameters.items():
        print('{k}: {a!r}'.format(k=k, a=v.annotation))
        print(v.annotation)
    print(sig.return_annotation)


check(foobar)
