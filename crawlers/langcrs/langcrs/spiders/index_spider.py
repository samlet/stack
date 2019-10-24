import scrapy

class IndexSpider(scrapy.Spider):
    """
    $ scrapy crawl index -o index.json
    $ scrapy crawl index -o index_ko.json -a tag=ko
    """
    name = "index"

    def start_requests(self):
        tag = getattr(self, 'tag', None)
        if tag is not None:
            langs=[tag]
        else:
            langs=['ro', 'ru']

        urls=[]
        for lang in langs:
            lang=lang.upper()
            urls.append(f"https://www.goethe-verlag.com/book2/EM/EM{lang}/EM{lang}002.HTM")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for col in response.css('div.col-md-4'):
            for tag in col.css("div a"):
                if tag.css('a span.gray::text').get() is not None:
                    yield {
                        'text': ''.join(tag.css('a::text').getall()).replace("\u00a0", ''),
                        'index': tag.css('a span.gray::text').get(),
                        'link': tag.css('a::attr(href)').get(),
                    }

