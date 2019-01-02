# procs-python-compile.md
⊕ [python - What's the difference between eval, exec, and compile? - Stack Overflow](https://stackoverflow.com/questions/2220699/whats-the-difference-between-eval-exec-and-compile)

    The compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1) built-in can be used to speed up repeated invocations of the same code with exec or eval by compiling the source into a code object beforehand. The mode parameter controls the kind of code fragment the compile function accepts and the kind of bytecode it produces. The choices are 'eval', 'exec' and 'single': ...

## reload
⊕ [imp — Access the import internals — Python 3.7.2 documentation](https://docs.python.org/3/library/imp.html#imp.reload)

```python
# work on module level
import singleton
import imp
imp.reload(singleton)
```

