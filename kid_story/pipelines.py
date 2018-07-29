# -*- coding: utf-8 -*-
import codecs
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class KidStoryPipeline(object):
    def process_item(self, item, spider):
        with codecs.open("my_data.txt", 'a', 'utf-8') as fp:
            fp.write(item['title'] + '===========\n' + item['content'] + '\n\n')
