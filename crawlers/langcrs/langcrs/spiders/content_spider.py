import scrapy


class ContentSpider(scrapy.Spider):
    name = "content"

    def start_requests(self):
        lang='RU'
        urls=[]
        for p in range(37,39):
            page=str(p).zfill(3)
            urls.append(f"https://www.goethe-verlag.com/book2/EM/EM{lang}/EM{lang}{page}.HTM")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # title part
        titles = response.css("div.col-md-4")
        title = titles[0]
        title_text=title.css('span.Stil36 b::text').get().strip()

        # content part
        table = response.css("div.col-md-12")
        cnt = table[2]
        index=0
        for row in cnt.css('tr'):
            # if row.css('td audio source::attr(src)').get() is not None:
            if row.css('td div.Stil35::text').get() is not None:
                index=index+1
                yield {
                    'chapter': title_text,
                    'index': index,
                    'text': row.css('td div.Stil35::text').get().strip(),
                    'translate': row.css(f'td div.Stil45 div#hn_{index} a::text').get().strip(),
                    'translit': row.css(f'td div.Stil45 div#hn_{index} span::text').get().strip(),
                    'audio': row.css('td audio source::attr(src)').get(),
                }

