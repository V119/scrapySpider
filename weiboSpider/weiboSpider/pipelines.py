# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from weiboSpider.items import *


class ImagePipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        global store_uri
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        if isinstance(item, UserInfoItem):
            if 'head_img_url' in item and item['head_img_url']:
                yield Request(item['head_img_url'])

        elif isinstance(item, BlogItem):
            # 获取微博中的图片
            if 'picture_url' in item and item['picture_url']:
                for pic_url in item['picture_url']:
                    yield Request(pic_url)

        elif isinstance(item, CommentItem):
            if 'img_url_list' in item and item['img_url_list']:
                for pic_url in item['img_url_list']:
                    yield Request(pic_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if isinstance(item, UserInfoItem):
            try:
                item['b_head_img_url'] = []
                path = store_uri + image_paths[0]
                fin = open(path, mode='br')
                img = fin.read()
                item['b_head_img_url'].append(img)
                fin.close()
            except IOError as e:
                print(e)
                raise IOError(e)

        elif isinstance(item, BlogItem):
            try:
                item['b_picture_url'] = []
                for path in image_paths:
                    path = store_uri + path
                    fin = open(path, mode='br')
                    img = fin.read()
                    item['b_picture_url'].append(img)
                    fin.close()
            except IOError as e:
                print(e)
                raise IOError(e)
        elif isinstance(item, CommentItem):
            try:
                item['b_img_url_list'] = []
                for path in image_paths:
                    path = store_uri + path
                    fin = open(path, mode='br')
                    img = fin.read()
                    item['b_img_url_list'].append(img)
                    fin.close()
            except IOError as e:
                print(e)
                raise IOError(e)

        return item


class ArticleImagePipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        global store_uri
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        if isinstance(item, BlogItem):
            if 'article_pic_url_desc' in item and item['article_pic_url_desc']:
                for key_url in item['article_pic_url_desc']:
                    yield Request(key_url)

    def item_completed(self, results, item, info):
        image_paths = [x for ok, x in results if ok]
        if isinstance(item, BlogItem):
            try:
                item['b_article_pic_url_dict'] = {}
                for result in image_paths:
                    path = store_uri + result['path']
                    fin = open(path, mode='br')
                    img = fin.read()
                    item['b_article_pic_url_dict'][result['url']] = img
                    fin.close()
            except IOError as e:
                print(e)
                raise IOError(e)

        return item


class SaveMysqlPipeline(object):
    def __init__(self, mysql_user_name, mysql_password, mysql_db):
        self.mysql_user_name = mysql_user_name
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_user_name=crawler.settings.get('MYSQL_USER_NAME'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.connect = mysql.connector.connect(
            user=self.mysql_user_name,
            password=self.mysql_password,
            database=self.mysql_db
        )

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        cursor = self.connect.cursor()

        sql = self.generate_insert_sql(item)
        if sql:
            cursor.execute(sql)
            self.connect.commit()

        cursor.close()
        return item

    def generate_insert_sql(self, item):
        if isinstance(item, UserInfoItem):
            tb_name = 'user_info'
        elif isinstance(item, FansItem):
            tb_name = 'fans'
        elif isinstance(item, BlogItem):
            tb_name = 'blog'
        elif isinstance(item, CommentItem):
            tb_name = 'comment'
        else:
            raise ValueError

        sql = 'INSERT INTO ' + tb_name + ' ('
        tb_fields = ''
        tb_values = ''
        for tb_f in item:
            if not tb_f.startswith('b_'):
                tb_fields = tb_fields + tb_f + ', '
                if isinstance(item[tb_f], str):
                    tb_values = tb_values + '"' + item[tb_f].replace('"', r'\"') + '", '
                else:
                    tb_values = tb_values + '"' + str(item[tb_f]) + '", '
        sql = sql + tb_fields[:-2] + ') VALUES (' + tb_values[:-2] + ')'

        return sql
