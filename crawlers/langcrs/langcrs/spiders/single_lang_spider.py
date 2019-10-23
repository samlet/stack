import scrapy


class SingleLangSpider(scrapy.Spider):
    name = "single_lang"
    start_urls = [
        'https://www.goethe-verlag.com/book2/EM/EMRO/EMRO002.HTM',
    ]

    def parse(self, response):
        for col in response.css('div.col-md-4'):
            for tag in col.css("div a"):
                yield {
                    'text': tag.css('a::text').getall(),
                    'index': tag.css('a span.gray::text').get(),
                    'link': tag.css('a::attr(href)').get(),
                }

