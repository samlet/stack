⊕ [Scrapy Tutorial — Scrapy 1.7.4 documentation](https://docs.scrapy.org/en/latest/intro/tutorial.html)

## start
```sh
scrapy startproject tutorial
```

+ tutorial/spiders/quotes_spider.py
    Subclass scrapy.Spider and define the initial requests to make.
    This is the code for our first Spider. Save it in a file named quotes_spider.py under the tutorial/spiders directory in your project:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
```

+ execute
    go to the project’s top level directory and run:

```sh
scrapy crawl quotes
scrapy crawl quotes_json -o quotes.json
# You can also use other formats, like JSON Lines:
scrapy crawl quotes_json -o quotes.jl
```



