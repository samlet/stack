# procs-corenlp-routines.md
## start
```python
## viz - 1
from sagas.nlu.corenlp_helper import CoreNlp, CoreNlpViz, get_nlp
ana=lambda sents: CoreNlpViz().analyse(sents, get_nlp('de'))
ana('Ich möchte, dass du ein Lehrer wirst.')

## viz - 2
from sagas.nlu.corenlp_helper import LangDialect
LangDialect('ko').ana('나는 중국 출신이다.')

## viz - 3
from sagas.nlu.corenlp_helper import LangDialect as dia
dia('pl').ana('śpiewasz piosenkę.')  # with word translation

## viz - 4
import sagas
sagas.dia('ru').ana_s('В шкафу много чашек?')

## viz - 5
import sagas
# ana=lambda s: sagas.dia('tr').ana(s)
ana=lambda s: sagas.dia('tr').ana_s(s)
ana('Kitabın yazarı makarna yer.')

## change viz display
from sagas.nlu.google_translator import get_word_map
from sagas.nlu.corenlp_helper import CoreNlp, CoreNlpViz, get_nlp

ana=lambda sents: CoreNlpViz(shape='ellipse', size='8,5', fontsize=20).analyse(sents, get_nlp('ar'), 
                                       get_word_map('ar','en', sents))
ana('أنا طالب جامعي صيني')
```

## uni_viz
```python
from sagas.nlu.uni_remote_viz import viz_sample
sents='what time is it ?'
viz_sample('en', sents)

# with translit
viz_sample('fa', 'الان تنیس بازی میکنم', translit_lang='fa')
# with translit and contrast
viz_sample('fa', '‫چه شماره ای را گرفتید؟‬', translit_lang='fa', enable_contrast=True)
```

+ env

```python
from sagas.nlu.uni_remote_viz import viz_sample
from sagas.nlu.env import sa_env
sa_env.runtime='jupyter'
viz_sample('fa', 'الان تنیس بازی میکنم', translit_lang='fa', enable_contrast=False)
```




