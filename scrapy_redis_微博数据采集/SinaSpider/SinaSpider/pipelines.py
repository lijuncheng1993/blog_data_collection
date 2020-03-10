# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

class SinaspiderPipeline(object):
    def __init__(self):
        client=pymongo.MongoClient(host='127.0.0.1',port=27017)
        db=client['Sina']
        self.Information=db['Information']

    def process_item(self, item, spider):
        self.Information.insert(dict(item))
        return item
