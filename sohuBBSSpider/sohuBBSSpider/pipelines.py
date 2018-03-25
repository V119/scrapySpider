# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from sohuBBSSpider.items import PostItem, CommentItem, AuthorItem, FansItem
from sohuBBSSpider.utils.gen_db_put import gen_start_spider_info, gen_author_put, gen_post_put, gen_comment_put, \
    gen_fans_put
from sohuBBSSpider.utils.gen_db_put import gen_stop_spider_info


class ImagePipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        global store_uri
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        if isinstance(item, (PostItem, CommentItem)) and 'picture_hrefs' in item and item['picture_hrefs']:
            for picture_url in item['picture_hrefs']:
                yield Request(picture_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        local_uri = [store_uri + image_path for image_path in image_paths]

        if isinstance(item, (PostItem, CommentItem)):
            item['picture_path'] = local_uri

        return item


class SaveHBasePipeline(object):
    def __init__(self, settings):
        self.DB_URI = settings['HBASE_URI']
        self.DB_PORT = settings['HBASE_PORT']
        self.TB_INFO = settings['TB_INFO'].encode()
        self.TB_POST = settings['TB_POST'].encode()
        self.TB_AUTHOR = settings['TB_AUTHOR'].encode()
        self.TB_COMMENT = settings['TB_COMMENT'].encode()
        self.TB_FANS = settings['TB_FANS'].encode()

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
        # noinspection PyBroadException
        try:
            self.client.put(self.TB_INFO, stop_put)
        except Exception:
            print('close spider put failure!')
            self.transport.close()
            self.transport.open()
            self.client.put(self.TB_INFO, stop_put)
        self.transport.close()

    def process_item(self, item, spider):
        table = None
        item_put = None
        if isinstance(item, AuthorItem):
            _, item_put = gen_author_put(item)
            table = self.TB_AUTHOR
        elif isinstance(item, PostItem):
            _, item_put = gen_post_put(item)
            table = self.TB_POST
        elif isinstance(item, CommentItem):
            _, item_put = gen_comment_put(item)
            table = self.TB_COMMENT
        elif isinstance(item, FansItem):
            _, item_put = gen_fans_put(item)
            table = self.TB_FANS
        # noinspection PyBroadException
        if table:
            try:
                self.client.put(table, item_put)
            except Exception:
                print('news item put failure!')
                self.transport.close()
                self.transport.open()
                self.client.put(table, item_put)

        return item
