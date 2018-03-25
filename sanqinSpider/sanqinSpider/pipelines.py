# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from hbase import THBaseService
from hbase.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

from sanqinSpider.utils.gen_db_put import *


class ImagePipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        global store_uri
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        if 'picture_urls' in item.fields and item['picture_urls']:
            for picture_url in item['picture_urls']:
                yield Request(picture_url)

    def item_completed(self, results, item, info):
        image_paths = [x for ok, x in results if ok]
        item['b_pictures'] = []
        for image_path in image_paths:
            try:
                path = image_path['path']
                url = image_path['url']

                path = store_uri + path

                fin = open(path, mode='br')
                img = fin.read()
                item['b_pictures'][url].append(img)
                fin.close()

                if os.path.exists(path):
                    os.remove(path)
            except IOError as e:
                print(e)
                raise IOError(e)

        return item


class SaveHBasePipeline(object):
    def __init__(self, settings):
        self.DB_URI = settings['HBASE_URI']
        self.DB_PORT = settings['HBASE_PORT']
        self.TB_INFO = settings['TB_INFO'].encode()
        self.TB_NEWS = settings['TB_NEWS'].encode()

        # 连接数据库表
        socket = TSocket.TSocket(self.DB_URI, self.DB_PORT)
        self.transport = TTransport.TFramedTransport(socket)
        protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.client = THBaseService.Client(protocol)

        self.transport.open()
        # 将爬虫开始的信息存入数据库
        self.spider_info_row_key, start_put = gen_start_spider_info()
        self.client.put(self.TB_INFO, start_put)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.spider.settings
        return cls(settings=settings)

    def close_spider(self, spider):
        # 存储爬虫结束的信息
        stop_put = gen_stop_spider_info(self.spider_info_row_key)
        try:
            self.client.put(self.TB_INFO, stop_put)
        except Exception as e:
            print('close spider put failure!' + e)
            self.transport.close()
            self.transport.open()
            self.client.put(self.TB_INFO, stop_put)
        self.transport.close()

    def process_item(self, item, spider):
        if isinstance(item, Declaration):
            _, item_put = gen_news_put(item)
            # noinspection PyBroadException
            try:
                self.client.put(self.TB_NEWS, item_put)
            except Exception as e:
                print('news item put failure!' + e)
                self.transport.close()
                self.transport.open()
                self.client.put(self.TB_NEWS, item_put)

