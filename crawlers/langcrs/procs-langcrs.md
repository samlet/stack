## start
```sh
$ using bigdata
# get index pages
$ scrapy crawl index -o index.json

# get content pages
$ scrapy crawl content -o content.json
```

## data visual
+ procs-scrapy.ipynb

```python
import pandas as pd
dfjson = pd.read_json('crawlers/langcrs/content.json')
dfjson
```

