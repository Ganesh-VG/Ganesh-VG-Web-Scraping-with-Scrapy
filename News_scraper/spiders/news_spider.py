import scrapy
import re
from scrapy.http import Request
from News_scraper.items import NewsScraperItem


class NewsSpider(scrapy.Spider):
    """"Spider class that scrape the News website to extract the required
    data from the news articles and save it into their respective JSON files"""

    name = 'getnews'  # Name of spider

    def __init__(self, url=None, *args, **kwargs):
        """Class initialization function to except the attribute 'url'"""
        super(NewsSpider, self).__init__(*args, **kwargs)
        self.url = url.strip()
        self.news_url = []

    def start_requests(self):
        """Start requests function to manually select URL from config.py"""
        url_first = self.url
        # sending url into the parse function through user agents like chrome, firefox etc
        yield Request(url_first, callback=self.parse, headers={'User-Agent': self.settings.get('USER_AGENT')})

    def parse(self, response):
        """Parse the website to extract categorical URL"""
        self.logger.info(f"Successfully crawled: {response.url}")

        self.base_url = response.url  # To get the URl that is currentl running

        cat_urls = response.css('a::attr(href)').getall()
        category_url = list(set(cat_urls))  # Avoids repetition

        # Match the general categorical URL pattern to avoid redundant scraping.
        pattern_c = re.compile(
            rf'^({self.base_url}|/)(([a-zA-Z\-]+/([a-zA-Z\-]+$|[a-zA-Z\-]+/$))|([a-zA-Z\-]+$|[a-zA-Z\-]+/$))')
        filtered_category_url = [c_url for c_url in category_url if pattern_c.match(c_url)]

        # Check for the proper format of the URL and send it for further processing.
        for filter_categ in filtered_category_url:
            if self.base_url not in filter_categ:
                filter_categ = self.base_url + filter_categ.strip().lstrip("/")

            yield response.follow(filter_categ, self.parse_category)

    def parse_category(self, response):
        """Parse each category to extract article URL"""
        local_news_url = []

        feeds_urls = response.css('a::attr(href)').getall()

        for feeds_url in feeds_urls:
            if feeds_url not in self.news_url:
                self.news_url.append(feeds_url)  # Avoid article URL repetition
                local_news_url.append(feeds_url)

        # Match the general article URL pattern to avoid redundant scraping.
        pattern_n = re.compile(
            rf'^({self.base_url}|/)[A-Za-z0-9\-_\₹/\!\@\#\$\%\^\&\*\(\)\+\=\{{}}\[\]\|\\\:\;\"\'\<\>\,\.\?\/\~\`]+([0-9]{{7}}/|-\d{{2}}|.html|.htm|[0-9]{{7}}|[a-zA-Z0-9\-]|[a-zA-Z0-9\-]/)$')
        filtered_news_url_re = [n_url for n_url in local_news_url if pattern_n.match(n_url)]

        # Remove unnecessary articles from the list.
        elements = ['/feedback', '/authors', '/author', '/userfeedback', '/video', '/rssfeed', '/videos', '/watch',
                    '/listen', '/prime', '/premium', '/photo', '/photos', '/cartoon', '/select/']
        filtered_news_url = [s for s in filtered_news_url_re if not any(e in s for e in elements)]

        # This is to ensure all URL's are in right format and send it for article parsing.
        for filtered_news in filtered_news_url:
            if self.base_url not in filtered_news:
                filtered_news = self.base_url + filtered_news.strip().lstrip("/")

            yield response.follow(filtered_news, self.parse_article)

    def parse_article(self, response):
        """Parse each article to extract required information"""
        try:
            # Match date pattern in the response.
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

            # Match title format in the response.
            title_match = response.xpath("//title/text()").get() or response.xpath("//h1/text()").get()

            # check if the response contain title and publish date to avoid redundant data.
            if title_match and match_date:
                item = NewsScraperItem()

                item['article_url'] = response.url

                item['title'] = title_match.strip()

                item['published_date'] = match_date

                # Extract author link first by matching regex if not found, then with xpath.
                author_link = next(
                    (
                        (
                            self.base_url + text.strip().lstrip("/")
                            if self.base_url not in text.strip() else text.strip()
                        )
                        for text in response.css('a::attr(href)').getall()
                        if re.compile(
                        rf'^({self.base_url}|/)((authors|author|agency)|[a-zA-Z0-9\-./]+/(authors|author))/[a-zA-Z0-9\-/]+').match(
                        text.strip())
                    ),
                    re.sub(r'\s+', ' ',
                           response.xpath('//*[contains(@class, "author")]/text()').get() or
                           response.xpath('//*[contains(@class, "premiumauthor")]/text()').get() or
                           response.xpath('//*[contains(@class, "article_author")]/text()').get() or
                           response.xpath('//a[contains(@class, "Author-authorName")]/@href').get() or
                           response.xpath('//*[contains(@class, "author-name")]/text()').get() or
                           response.xpath('//*[contains(@class, "brand-detial-main")]//span/text()').get() or
                           response.xpath('//*[contains(@class, "publisher")]/text()').get() or
                           response.xpath('//span[@class="byline__names"]/text()').get() or
                           response.xpath('//span[@class="ag"]/text()').get() or "").strip() or "Not Available"
                )

                # Extract author name and author URL.
                if "https://" in author_link or "Https://":

                    # If 'author_link' is a URL than extract the author name from it using following code
                    author_name = " ".join(
                        zl for zl in (author_link.strip("/").split("/")[-1].replace("-", " ")).split(" ") if
                        zl.isalpha())

                    # If 'author_link' is a URL than just save it as author url
                    author_url = author_link

                else:
                    # If its not a URL then it will be a author name that is extracted.
                    author_name = author_link

                    # URL is not present for author in the website
                    author_url = "Not Available"

                # store author name
                item['author_name'] = author_name.title()

                final_autor_url_check = [author_url_response for author_url_response in
                                         response.css('a::attr(href)').getall() if
                                         ("-".join(author_name.split(" "))) in author_url_response]

                # store author URL
                item['author_url'] = author_url if author_url != author_name else final_autor_url_check[
                    0] if final_autor_url_check else 'Not Available'

                # Clean and concatenate article content and store it
                paragraphs = (response.xpath("//p//text()").getall() or
                              response.xpath(
                                  "//article//div//h2//text() | //article//div//h3//text() | //article//div//h4//text() | //article//div//h5//text() | //article//div//h6//text()").getall() or
                              response.xpath(
                                  "//article//h2//text() | //article//h3//text() | //article//h4//text() | //article//h5//text() | //article//h6//text()").getall() or
                              response.xpath("//article//div//text()").getall()
                              )
                item['article_content'] = re.sub(r'\s+', ' ', ' '.join(paragraphs)).strip()

                yield item

        except AttributeError:
            print("//////////  THIS IS NOT A NEWS ARTICLE  ///////////")
