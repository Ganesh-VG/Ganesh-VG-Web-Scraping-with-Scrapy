# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import re
from config import WEBSITE_URL


class NewsScraperPipeline:
    def open_spider(self, spider):
        # extract the website name to assign to the JSON file name
        website = re.search(r'https://([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|in|co\.uk|org|net|gov|edu|us|au|ca|'
                            r'de|fr|jp|ru|ch|it|nl|se|no|es|mil|int|info|biz|name|pro|io|co|tv|me|ly|club|news|media|co'
                            r'\.in|co\.jp|co\.kr|co\.za|co\.br|co\.id|co\.th|co\.sg|co\.hk|co\.ph|co\.my|co\.nz|co\.uk)'
                            , WEBSITE_URL).group(1)

        # Open the JSON file inorder to save the data
        self.file = open(f'JSON_files/{website}_articles.json', 'w', encoding='utf-8')
        self.file.write('[\n')  # Start of the JSON array

    def close_spider(self, spider):
        # Move the file pointer to the position before the last comma and newline
        self.file.seek(self.file.tell() - 3, 0)
        self.file.write('\n]')  # End of the JSON array
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.file.write(line + ',\n')  # Add a comma and newline after each item
        return item
