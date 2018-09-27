import csv
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DigikalacrawlerPipeline(object):
    pass
    # def open_spider(self, spider):
    #     self.file = open('{}.csv'.format(spider.name), 'w')
    #     self.writer = csv.writer(self.file)
    #
    # def close_spider(self, spider):
    #     self.file.close()
    #
    # def process_item(self, item, spider):
    #     self.writer.writerow(item)
    #     return item


    # def process_item(self, item, spider):
    #     line = json.dumps(dict(item)) + "\n"
    #     self.file.write(line)
    #     return item
    #
    # def process_item(self, item, spider):
    #     if not getattr(spider, 'csv', False):
    #         return item
    #     with open('{}.csv'.format(spider.name), 'a') as f:
    #         writer = csv.writer(f)
    #         writer.writerow(item)
    #     return item
