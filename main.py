import os
import asyncio
from twisted.internet import asyncioreactor

# Set the event loop policy to use SelectorEventLoop on Windows
if os.name == 'nt':
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)

# Install the asyncio reactor
asyncioreactor.install()

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from News_scraper.spiders.news_spider import NewsSpider

def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings=settings)

    async def run_spider(url):
        await runner.crawl(NewsSpider, url=url)

    async def main_crawl():
        with open('config.txt', 'r') as file:
            urls = [line.strip() for line in file.readlines()]

        max_concurrent_tasks = 5  # Start with 3, you can increase to 5 after testing
        semaphore = asyncio.Semaphore(max_concurrent_tasks)

        async def sem_run_spider(url):
            async with semaphore:
                await run_spider(url)

        tasks = [sem_run_spider(url) for url in urls]
        await asyncio.gather(*tasks)
        reactor.stop()

    reactor.callLater(0, lambda: asyncio.ensure_future(main_crawl()))
    reactor.run()

if __name__ == '__main__':
    main()
