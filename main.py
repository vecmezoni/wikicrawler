import json
import time
from dataclasses import dataclass

from scrapy.crawler import CrawlerProcess

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
import psycopg2

POSTGRES = {
    'user': 'postgres',
    'password': 'postgres',
    'dbname': 'postgres',
    'host': 'postgres',
}


@dataclass
class WikiItem:
    id: str
    title: str
    language: str
    url: str


class WikiSpider(CrawlSpider):
    name = 'wikispider'
    allowed_domains = ['m.wikipedia.org']
    start_urls = ['https://en.m.wikipedia.org/wiki/Piano_Sonata_No._31_(Beethoven)']
    rules = (
        Rule(LinkExtractor(allow=r'/wiki/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        try:
            metadata = json.loads(response.css('script[type="application/ld+json"]::text').get())
        except:
            return

        id = metadata.get('mainEntity').split('/')[-1]
        title = metadata.get('name')
        language = response.css('html::attr(lang)').get()

        if not id or not title or not language:
            return

        item = WikiItem(
            id=id,
            title=title,
            language=language,
            url=response.url,
        )

        return item


class PostgresPipeline:
    def __init__(self):
        self.conn = None

    def open_spider(self, spider):
        self.conn = psycopg2.connect(**POSTGRES)

    def close_spider(self, spider):
        self.conn.close()
        self.conn = None

    def process_item(self, item, spider):
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute('''
                        insert into article ( id, title, language, url )
                        values (%s, %s, %s, %s) ON CONFLICT DO NOTHING;
                        ''', (
                    item.id,
                    item.title,
                    item.language,
                    item.url))
        return item


if __name__ == '__main__':
    while (True):
        try:
            conn = psycopg2.connect(**POSTGRES)
            conn.close()
            break
        except:
            time.sleep(5)

    process = CrawlerProcess(settings={
        'ITEM_PIPELINES': {PostgresPipeline: 300, },
        'LOG_LEVEL': 'INFO'
    })

    process.crawl(WikiSpider)
    process.start()
