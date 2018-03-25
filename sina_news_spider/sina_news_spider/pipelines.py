# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline


class SaveImagePipeline(ImagesPipeline):
    @classmethod
    def from_settings(cls, settings):
        global store_uri
        store_uri = settings['IMAGES_STORE']
        return cls(store_uri, settings=settings)

    def get_media_requests(self, item, info):
        if 'picture_urls' in item and item['picture_urls']:
            for picture_url in item['picture_urls']:
                yield Request(picture_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        item['b_pictures'] = []
        item['picture_local_path'] = []
        for image_path in image_paths:
            try:

                path = store_uri + image_path

                fin = open(path, mode='br')
                img = fin.read()
                item['b_pictures'].append(img)
                item['picture_local_path'].append(path)
                fin.close()

                # if os.path.exists(path):
                #     os.remove(path)
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
        tb_name = 'news'

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
