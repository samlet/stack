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

+ svg
    * http://www.xavierdupre.fr/app/jyquickhelper/helpsphinx/notebooks/notebook_html_svg.html#svg

```python
from IPython.display import SVG
SVG("""<svg>
    <rect x="10" y="10" height="100" width="100"
          style="stroke:#ff0000; fill: #0000ff"/>
</svg>""")
```

+ env

```python
from sagas.nlu.uni_remote_viz import viz_sample
from sagas.nlu.env import sa_env
sa_env.runtime='jupyter'
viz_sample('fa', 'الان تنیس بازی میکنم', translit_lang='fa', enable_contrast=False)
```

+ tracker

```python
from sagas.tracker_jupyter import enable_jupyter_tracker
from sagas.nlu.nlu_tools import NluTools
enable_jupyter_tracker()
tools=NluTools()
tools.clip_parse('fi', 'Tuolla ylhäällä asuu vanha nainen.')
```

