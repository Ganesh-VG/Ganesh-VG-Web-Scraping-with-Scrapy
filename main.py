import os
import time
import asyncio
from twisted.internet import asyncioreactor

# Set the event loop policy to use SelectorEventLoop on Windows
if os.name == 'nt':
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)

# Install the asyncio reactor
asyncioreactor.install()

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from News_scraper.spiders.news_spider import NewsSpider

def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings=settings)

    @defer.inlineCallbacks
    def crawl():
        with open('config.txt', 'r') as file:
            urls = [line.strip() for line in file.readlines()]
        for url in urls:
            time.sleep(60)
            yield runner.crawl(NewsSpider, url=url)
            time.sleep(10)
        reactor.stop()

    crawl()
    reactor.run()

if __name__ == '__main__':
    main()
