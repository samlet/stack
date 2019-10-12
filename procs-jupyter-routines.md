# procs-jupyter-routines.md
## python
```python
import importlib
import sagas.tool.loggers
importlib.reload(sagas.tool.loggers)
```
```python
%load_ext autoreload
%autoreload 2
# %autoreload 2 Reload all modules (except those excluded by %aimport) every time before executing the Python code typed.
```

+ env

```python
from sagas.nlu.uni_remote_viz import viz_sample
from sagas.nlu.env import sa_env
sa_env.runtime='jupyter'
viz_sample('fa', 'الان تنیس بازی میکنم', translit_lang='fa', enable_contrast=False)
```


