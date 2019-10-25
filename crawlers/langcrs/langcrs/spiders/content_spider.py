import scrapy


class ContentSpider(scrapy.Spider):
    """
    $ scrapy crawl content -o content.json
    $ scrapy crawl content -o sample_fa.json -a tag=fa -a limit=1
    $ scrapy crawl content -o content_ko.json -a tag=ko
    $ scrapy crawl content -o content_ru.json -a tag=ru
    $ scrapy crawl content -o content_fr.json -a tag=fr -a limit=10
    $ start cr ja       # crawl the top 10 pages to content_{lang}.json
    $ start cr100 he    # crawl all pages for special language to all_{lang}.json
    """
    name = "content"

    def start_requests(self):
        if self.limit is not None:
            print(f'.. {self.limit}')
            limit=int(self.limit)
        else:
            limit = 2

        tag = getattr(self, 'tag', None)
        if tag is not None:
            lang = tag.upper()
        else:
            lang = 'RU'

        self.lang=lang.lower()
        urls=[]
        start=1
        offset=2

        # for p in range(start,start+10):
        for p in range(start+offset, start + offset+limit):
        # for p in range(37, 39):
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

                if self.lang in ('fa', 'ar', 'ur', 'hy'):
                    yield {
                        'chapter': title_text,
                        'index': index,
                        'text': row.css('td div.Stil35::text').get().strip(),
                        'translate': row.css('td div.Stil45::text').get().strip(),
                        'translit': row.css('td div.Stil45 span::text').get().strip(),
                        'audio': row.css('td audio source::attr(src)').get(),
                    }
                else:
                    translit=row.css(f'td div.Stil45 div#hn_{index} span::text').get()
                    if translit is not None:
                        translit_text=translit.strip()
                    else:
                        translit_text=''

                    yield {
                        'chapter': title_text,
                        'index': index,
                        'text': row.css('td div.Stil35::text').get().strip(),
                        'translate': row.css(f'td div.Stil45 div#hn_{index} a::text').get().strip(),
                        'translit': translit_text,
                        'audio': row.css('td audio source::attr(src)').get(),
                    }

