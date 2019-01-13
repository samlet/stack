# procs-python-dev-tool.md
⊕ [sha256/python-var-dump: PHP's var_dump equivalent function for Python](https://github.com/sha256/python-var-dump)
⊕ [pprint — Data pretty printer — Python 3.7.2 documentation](https://docs.python.org/3/library/pprint.html)

## var_dump
```sh
pip install var_dump
```
```python
from var_dump import var_dump

var_dump(123)                   # output: #0 int(123)
var_dump(123.44)                # output: #0 float(123.44)
var_dump("this is a string")    # output: #0 str(16) "this is a string"
var_dump(None) # output:        # output: #0 NoneType(None)
var_dump(True) # output         # output: #0 bool(True)

var_dump(123, 123.44, None, False)
```

