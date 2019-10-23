import scrapy


class IndexSpider(scrapy.Spider):
    name = "index"

    def start_requests(self):
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
                yield {
                    'text': tag.css('a::text').getall(),
                    'index': tag.css('a span.gray::text').get(),
                    'link': tag.css('a::attr(href)').get(),
                }

