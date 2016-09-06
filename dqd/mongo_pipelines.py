# -*- coding:utf-8 -*-
import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings
# from scrapy import log


class MongoDBPipeline(object):
    #Connect to the MongoDB database
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]



    def process_item(self, item, spider):
        valid=True
        for data in item:
            if not data:
                valid=False
                raise DropItem('Missing{0}!'.format(data))
        if valid:

            self.collection.insert(dict(item))
            log.msg('question added to mongodb database!',
                    level=log.DEBUG,spider=spider)
        return item