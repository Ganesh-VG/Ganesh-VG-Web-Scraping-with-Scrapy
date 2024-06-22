import os
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from News_scraper.spiders.news_spider import NewsSpider
import time

def main():
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        with open('config.txt', 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        for url in urls:
            yield runner.crawl(NewsSpider, url=url)
            time.sleep(10)
        reactor.stop()

    crawl()
    reactor.run()

if __name__ == '__main__':
    main()
