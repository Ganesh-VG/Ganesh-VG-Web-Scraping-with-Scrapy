# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import re

class NewsScraperPipeline:
    def __init__(self):
        self.files = {}

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        for file in self.files.values():
            file.seek(file.tell() - 3, 0)
            file.write('\n]')
            file.close()

    def open_website_file(self, website):
        if website not in self.files:
            if website:
                self.files[website] = open(f'JSON_files/{website}_articles.json', 'w', encoding='utf-8')
                self.files[website].write('[\n')

    def process_item(self, item, spider):
        website = re.search(r'https?://(?:www\.)?([a-zA-Z0-9-]+)\.', item['article_url']).group(1)
        self.open_website_file(website)
        line = json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.files[website].write(line + ',\n')
        return item
