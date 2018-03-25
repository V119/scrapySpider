# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from pprint import pformat

import scrapy


class NewsItem(scrapy.Item):
    url = scrapy.Field()
    news_type = scrapy.Field()
    path_text = scrapy.Field()                  # 路径文字
    path_url = scrapy.Field()                   # 路径URL
    key_words = scrapy.Field()                  # 关键字
    tags = scrapy.Field()                       # 标签
    news_id = scrapy.Field()                    # 新闻的ID
    title = scrapy.Field()                      # 标题
    description = scrapy.Field()                # 简介
    date_time = scrapy.Field()                  # 日期时间
    comment_id = scrapy.Field()                 # 评论的ID
    author = scrapy.Field()                     # 作者
    editor = scrapy.Field()                     # 编辑
    from_media = scrapy.Field()                 # 来自
    from_media_url = scrapy.Field()             # 来自的URL
    content = scrapy.Field()                    # 内容
    picture_urls = scrapy.Field()               # 图片
    participant_num = scrapy.Field()            # 参与数量

    b_pictures = scrapy.Field()
    picture_local_path = scrapy.Field()

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)

    def __str__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)

class CommentItem(scrapy.Item):
    pass
