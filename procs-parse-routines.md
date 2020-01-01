# procs-parse-routines.md
## free
```python
from sagas.nlu.ruleset_procs import list_words, cached_chunks
from sagas.conf.conf import cf
from sagas.tracker_jupyter import enable_jupyter_tracker
enable_jupyter_tracker()

# There are not many trees in the desert.
sents='Tidak banyak pohon di gurun.'
lang='id'
domain='root_domains'
chunks = cached_chunks(sents, lang, cf.engine(lang))
domains = chunks[domain]
domains
```
```python
from sagas.nlu.uni_remote_viz import list_contrast, display_doc_deps
display_doc_deps(chunks['doc'], None)
```


