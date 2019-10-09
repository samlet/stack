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



