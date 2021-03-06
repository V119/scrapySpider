# # -*- coding: utf-8 -*-
#
# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from scrapy import Request
# from scrapy.pipelines.images import ImagesPipeline
#
#
# # noinspection PyGlobalUndefined
# from kdnetSpider.items import PostItem, CommentItem, AuthorItem, FansItem
#
# from hbase import THBaseService
# from hbase.ttypes import *
# from thrift.transport import TSocket
# from thrift.transport import TTransport
# from thrift.protocol import TCompactProtocol
#
# from kdnetSpider.utils.gen_db_put import gen_stop_spider_info, gen_start_spider_info, gen_author_put, gen_post_put, \
#     gen_comment_put, gen_fans_put
#
#
# class ImagePipeline(ImagesPipeline):
#     @classmethod
#     def from_settings(cls, settings):
#         global store_uri
#         store_uri = settings['IMAGES_STORE']
#         return cls(store_uri, settings=settings)
#
#     def get_media_requests(self, item, info):
#         if 'pictures_href' in item and item['pictures_href']:
#             for picture_url in item['pictures_href']:
#                 yield Request(picture_url)
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#
#         local_uri = [store_uri + image_path for image_path in image_paths]
#
#         if isinstance(item, (PostItem, CommentItem)):
#             item['pictures_local_uri'] = local_uri
#
#         return item
#
#
# class SaveHBasePipeline(object):
#     def __init__(self, settings):
#         self.DB_URI = settings['HBASE_URI']
#         self.DB_PORT = settings['HBASE_PORT']
#         self.TB_INFO = settings['TB_INFO'].encode()
#         self.TB_NEWS = settings['TB_NEWS'].encode()
#
#         # 连接数据库表
#         socket = TSocket.TSocket(self.DB_URI, self.DB_PORT)
#         self.transport = TTransport.TFramedTransport(socket)
#         protocol = TCompactProtocol.TCompactProtocol(self.transport)
#         self.client = THBaseService.Client(protocol)
#
#         self.transport.open()
#         # 将爬虫开始的信息存入数据库
#         self.spider_info_row_key, start_put = gen_start_spider_info()
#         self.client.put(self.TB_INFO, start_put)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         settings = crawler.spider.settings
#         return cls(settings=settings)
#
#     def close_spider(self, spider):
#         # 存储爬虫结束的信息
#         stop_put = gen_stop_spider_info(self.spider_info_row_key)
#         # noinspection PyBroadException
#         try:
#             self.client.put(self.TB_INFO, stop_put)
#         except Exception:
#             print('close spider put failure!')
#             self.transport.close()
#             self.transport.open()
#             self.client.put(self.TB_INFO, stop_put)
#         self.transport.close()
#
#     def process_item(self, item, spider):
#         if isinstance(item, AuthorItem):
#             _, item_put = gen_author_put(item)
#         elif isinstance(item, PostItem):
#             _, item_put = gen_post_put(item)
#         elif isinstance(item, CommentItem):
#             _, item_put = gen_comment_put(item)
#         elif isinstance(item, FansItem):
#             _, item_put = gen_fans_put(item)
#         # noinspection PyBroadException
#         try:
#             self.client.put(self.TB_NEWS, item_put)
#         except Exception:
#             print('news item put failure!')
#             self.transport.close()
#             self.transport.open()
#             self.client.put(self.TB_NEWS, item_put)
