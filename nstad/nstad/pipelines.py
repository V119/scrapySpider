# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from nstad.items import *

import mysql.connector


class SavePipeline(object):
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
            try:
                cursor.execute(sql)
                self.connect.commit()
            except:
                raise ValueError(sql)

        cursor.close()
        return item

    def generate_insert_sql(self, item):
        if isinstance(item, NewsItem):
            sql = '''INSERT INTO tb_news (TITLE,
                                             DATE,
                                             SOURCE,
                                             CONTENT
                                             )
                      VALUES ("%s", "%s", "%s", "%s")
            ''' % (item['title'].replace('"', '\\\"'),
                   item['date'],
                   item['source'],
                   item['content'].replace('"', '\\\"')
                   )
            return sql
        elif isinstance(item, PolicyItem):
            sql = '''INSERT INTO tb_policy (TITLE,
                                          DATE,
                                          SOURCE,
                                          CONTENT,
                                          CATEGORY
                                          )
                     VALUES ("%s", "%s", "%s", "%s", "%s")
                        ''' % (item['title'].replace('"', '\\\"'),
                               item['date'],
                               item['source'],
                               item['content'].replace('"', '\\\"'),
                               item['category']
                               )
            return sql
        elif isinstance(item, ResultItem):
            sql = '''INSERT INTO tb_result (TITLE,
                                            DATE,
                                            PID,
                                            KEY_WORDS,
                                            DESCRI
                                            )
                     VALUES ("%s", "%s", "%s", "%s", "%s")
            ''' % (item['title'].replace('"', '\\\"'),
                   item['date'],
                   item['pid'],
                   item['key_words'].replace('"', '\\\"') if item['key_words'].replace('"', '\\\"') else ' ',
                   item['desc'].replace('"', '\\\"')
                   )
            return sql
