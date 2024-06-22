import scrapy
import re
from scrapy.http import Request
from News_scraper.items import NewsScraperItem
from config import WEBSITE_URL


class NewsSpider(scrapy.Spider):
    """"Spider class that scrape the News website
    to extract the required data from the news articles
    and save it into their respective JSON files"""

    name = 'getnews'  # Name of spider
    news_url = []

    # def start_requests(self):
    #     """Start requests function to manually select URL from config.py"""
    #     url = WEBSITE_URL
    #     yield Request(url, headers={'User-Agent': self.settings.get('USER_AGENT')})

    def __init__(self, url=None, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []


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
                filter_categ = self.base_url + filter_categ.strip().lstrip("/")

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
            if self.base_url not in filtered_news:
                filtered_news = self.base_url + filtered_news.strip().lstrip("/")

            # Pass on each categorical URL to parse the articles
            yield response.follow(filtered_news, self.parse_article)

    def parse_article(self, response):

        date_pattern = re.compile(
            r'\b(0?[1-9]|[12][0-9]|3[01])[-/.](Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|JAN(?:UARY)?|FEB(?:RUARY)?|MAR(?:CH)?|APR(?:IL)?|MAY|JUN(?:E)?|JUL(?:Y)?|AUG(?:UST)?|SEP(?:TEMBER)?|OCT(?:OBER)?|NOV(?:EMBER)?|DEC(?:EMBER)?)[-/.](\d{4})\b|'
            r'\b(0?[1-9]|[12][0-9]|3[01])\s+(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|JAN(?:UARY)?|FEB(?:RUARY)?|MAR(?:CH)?|APR(?:IL)?|MAY|JUN(?:E)?|JUL(?:Y)?|AUG(?:UST)?|SEP(?:TEMBER)?|OCT(?:OBER)?|NOV(?:EMBER)?|DEC(?:EMBER)?)\s+(\d{4})\b|'
            r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|JAN(?:UARY)?|FEB(?:RUARY)?|MAR(?:CH)?|APR(?:IL)?|MAY|JUN(?:E)?|JUL(?:Y)?|AUG(?:UST)?|SEP(?:TEMBER)?|OCT(?:OBER)?|NOV(?:EMBER)?|DEC(?:EMBER)?)\s+(0?[1-9]|[12][0-9]|3[01]),\s+(\d{4})\b|'
            r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?|JAN(?:UARY)?|FEB(?:RUARY)?|MAR(?:CH)?|APR(?:IL)?|MAY|JUN(?:E)?|JUL(?:Y)?|AUG(?:UST)?|SEP(?:TEMBER)?|OCT(?:OBER)?|NOV(?:EMBER)?|DEC(?:EMBER)?)\s+(0?[1-9]|[12][0-9]|3[01])\s+(\d{4})\b|'
            r'\b(0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])[-/](19\d\d|20\d\d)\b|'
            r'\b(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/](19\d\d|20\d\d)\b|'
            r'\b(19\d\d|20\d\d)[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b|'
            r'\b(0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])[-/](\d\d)\b|'
            r'\b(19\d\d|20\d\d)-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b'
        )
        match_date = (response.xpath('//time/@datetime').get() or date_pattern.search(response.text).group(0))

        title_match = response.xpath("//title/text()").get() or response.xpath("//h1/text()").get()

        if title_match and match_date:
            item = NewsScraperItem()

            item['article_url'] = response.url

            item['title'] = title_match.strip()

            item['published_date'] = match_date

            # Define author link
            author_link = next(
                (
                    # If the URL is not in right format this will correct it.
                    (
                        self.base_url + text.strip().lstrip("/")
                        if self.base_url not in text.strip() else text.strip()
                    )
                    # This is a list comprehension to extract the author URL
                    for text in response.css('a::attr(href)').getall()
                    if re.compile(
                    rf'^({self.base_url}|/)((authors|author|etreporter)|[a-zA-Z0-9\-/]+/(authors|author|etreporter))/[a-zA-Z0-9\-/]+').match(
                    text.strip())
                ),
                # If the first code in next function gives null as output than next code will run
                # This is the html parser to extract author name using css selectors
                re.sub(r'\s+', ' ',
                       response.xpath('//*[contains(@class, "author")]/text()').get() or
                       response.xpath('//*[contains(@class, "premiumauthor")]/text()').get() or
                       response.xpath('//*[contains(@class, "article_author")]/text()').get() or
                       response.xpath('//a[contains(@class, "Author-authorName")]/@href').get() or
                       response.xpath('//*[contains(@class, "author-name")]/text()').get() or
                       response.xpath('//*[contains(@class, "brand-detial-main")]//span/text()').get() or
                       response.xpath('//*[contains(@class, "publisher")]/text()').get() or
                       response.xpath('//span[@class="ag"]/text()').get() or "").strip() or "Not Available"
            )

            # Extract author name
            if "https://" in author_link or "Https://":

                # If 'author_link' is a URL than extract the author name from it using following code
                author_name = (author_link.strip("/").split("/")[-1].replace("-", " "))

                # If 'author_link' is a URL than just save it as author url
                author_url = author_link

            else:
                # If not than it will be a name extracted using css selector so store it in name.
                author_name = author_link

                # URL is not present for author in the website
                author_url = "Not Available"

            # store author name
            item['author_name'] = author_name.title()

            # store author URL
            item['author_url'] = author_url

            # Clean and concatenate article content and store it
            paragraphs = response.xpath(
                "//p//text() | //article//div//text() | //article//div//h2//text() | //article//div//h3//text() | //article//div//h4//text() | //article//div//h5//text() | //article//div//h6//text() | //article//h2//text() | //article//h3//text() | //article//h4//text() | //article//h5//text() | //article//h6//text()").getall()
            item['article_content'] = re.sub(r'\s+', ' ', ' '.join(paragraphs)).strip()

            yield item
