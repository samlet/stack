# procs-python-eval.md
+ procs-python-eval.ipynb
⊕ [Python: Way to speed up a repeatedly executed eval statement? - Stack Overflow](https://stackoverflow.com/questions/12467570/python-way-to-speed-up-a-repeatedly-executed-eval-statement)
⊕ [The exec Statement and A Python Mystery « late.am](https://late.am/post/2012/04/30/the-exec-statement-and-a-python-mystery.html)

You can also trick python:

```python
expression = "math.sin(v['x']) * v['y']"
exp_as_func = eval('lambda: ' + expression)
```
And then use it like so:

exp_as_func()

Speed test:

In [17]: %timeit eval(expression)
10000 loops, best of 3: 25.8 us per loop

In [18]: %timeit exp_as_func()
1000000 loops, best of 3: 541 ns per loop
As a side note, if v is not a global, you can create the lambda like this:

exp_as_func = eval('lambda v: ' + expression)
and call it:

exp_as_func(my_v)

+ You can avoid the overhead by compiling the expression in advance using  compiler.compile() for Python 2 or compile() for Python 3 :

```python
In [1]: import math, compiler

In [2]: v = {'x': 2, 'y': 4}

In [3]: expression = "math.sin(v['x']) * v['y']"

In [4]: %timeit eval(expression)
10000 loops, best of 3: 19.5 us per loop

In [5]: compiled = compiler.compile(expression, '<string>', 'eval')

In [6]: %timeit eval(compiled)
1000000 loops, best of 3: 823 ns per loop
```
Just make sure you do the compiling only once (outside of the loop). As mentioned in comments, when using eval on user submitted strings make sure you are very careful about what you accept.