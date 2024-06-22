# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScraperItem(scrapy.Item):
    article_url = scrapy.Field()
    title = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()
    article_content = scrapy.Field()
    published_date = scrapy.Field()
