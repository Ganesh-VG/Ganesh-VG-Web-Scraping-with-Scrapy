# main.py
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from News_scraper.spiders.news_spider import NewsSpider

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(NewsSpider)
    process.start()  # the script will block here until the crawling is finished
