import scrapy
import re
from scrapy.http import Request
from News_scraper.items import NewsScraperItem
from config import WEBSITE_URL


class NewsSpider(scrapy.Spider):
    name = 'getnews'
    news_url = []
    base_url = None

    def start_requests(self):
        url = WEBSITE_URL
        yield Request(url, headers={'User-Agent': self.settings.get('USER_AGENT')})

    def parse(self, response):
        self.logger.info(f"Successfully crawled: {response.url}")
        self.base_url = response.url
        cat_urls = response.css('a::attr(href)').getall()
        category_url = list(set(cat_urls))

        # print(category_url)

        pattern_c = re.compile(
            rf'^({self.base_url}|/)(([a-zA-Z\-]+/([a-zA-Z\-]+$|[a-zA-Z\-]+/$))|([a-zA-Z\-]+$|[a-zA-Z\-]+/$))')
        filtered_category_url = [c_url for c_url in category_url if pattern_c.match(c_url)]

        # print(filtered_category_url)

        for filter_categ in filtered_category_url:

            if self.base_url not in filter_categ:
                filter_categ = self.base_url + filter_categ

            yield response.follow(filter_categ, self.parse_category)

    def parse_category(self, response):
        local_news_url = []

        feeds_urls = response.css('a::attr(href)').getall()

        for feeds_url in feeds_urls:

            if feeds_url not in self.news_url:
                self.news_url.append(feeds_url)
                local_news_url.append(feeds_url)

        pattern_n = re.compile(
            rf'^({self.base_url}|/)[A-Za-z0-9\-_\₹/\!\@\#\$\%\^\&\*\(\)\+\=\{{}}\[\]\|\\\:\;\"\'\<\>\,\.\?\/\~\`]+([0-9]{{7}}/|-\d{{2}}|.html|.htm|[0-9]{{7}}|[a-zA-Z0-9\-]|[a-zA-Z0-9\-]/)$')

        # Filter news_url list using the pattern
        filtered_news_url = [n_url for n_url in local_news_url if pattern_n.match(n_url)]

        # print(filtered_news_url)

        # Parsing matched articles one after the other
        for filtered_news in filtered_news_url:

            # This is to ensure all URL's are in right format
            if filtered_news.startswith("/"):
                filtered_news = self.base_url + filtered_news

            # Pass on each categorical URL to parse the articles
            yield response.follow(filtered_news, self.parse_article)

    def parse_article(self, response):

        date_pattern = re.compile(
            r'\d{2} \b[A-Za-z]{3} \d{4}\b|\b[A-Za-z]{3} \d{2}, \d{4}\b|\b[A-Za-z]{3} \d{2} \d{4}\b|\d{2}-\d{2}-\d{4}|'
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{2}, \d{4}\b|'
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December) \d{2} \d{4}\b|'
            r'\d{2} \b(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b')
        match_date = (response.xpath('//time/@datetime').get() or date_pattern.search(response.text).group(0)
                      or 'No date found')

        title_match = response.xpath("//title/text()").get()

        if title_match and match_date:
            item = NewsScraperItem()

            item['article_url'] = response.url

            item['title'] = title_match

            item['published_date'] = match_date

            yield item
