## start
```sh
$ using bigdata
$ scrapy list

# get index pages
$ scrapy crawl index -o index.json
$ scrapy crawl index -o index_ko.json -a tag=ko

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

