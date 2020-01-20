# procs-parse-routines.md
## free
```python
from sagas.nlu.ruleset_procs import list_words, cached_chunks, get_main_domains
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
```python
from sagas.kit.analysis_kit import vis_domains
sents='What do you think about the war?'
lang='en'
domain='subj_domains' # 'verb_domains', 'aux_domains'
vis_domains(sents, lang, domain)

for v in vis_domains(sents, lang, domain, all_subsents=True):
    display(v)
for v in vis_domains(sents, lang, all_subsents=True):
    display(v)

from sagas.kit.analysis_kit import vis_domains
for v in vis_domains('What do you think about the war?', 'en', all_subsents=True): display(v)        
```



