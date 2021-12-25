import scrapy
from scrapy.crawler import CrawlerProcess


class WikiSpider(scrapy.Spider):
    name = 'wikispider'
    start_urls = ['https://en.wikipedia.org/wiki/Piano_Sonata_No._31_(Beethoven)']

    def parse(self, response, **kwargs):
        for language in response.css('html'):
            yield {'language': language.css('::attr(lang)').get()}

        for title in response.css('h1'):
            yield {'title': title.css('::text').get()}

        for next_page in response.css('a'):
            href = next_page.css('::attr(href)').get()
            if href and 'wikipedia.org/wiki/' in href:
                yield response.follow(href, self.parse)


if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEEDS': {
            'items.json': {'format': 'json'},
        },
    })

    process.crawl(WikiSpider)
    process.start()
