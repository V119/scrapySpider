# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import json

import scrapy


class NewsItem(scrapy.Item):
    url = scrapy.Field()                        # 文章的URL
    path_url = scrapy.Field()                   # 文章路径的URL
    path_text = scrapy.Field()                  # 文章路径的文本表示
    title = scrapy.Field()                      # 文章的标题
    publish_time = scrapy.Field()               # 文章的发表时间
    editor = scrapy.Field()                     # 文章的编辑
    abstract = scrapy.Field()                   # 核心提示
    source_text = scrapy.Field()                # 来源
    source_href = scrapy.Field()                # 来源URL
    picture_urls = scrapy.Field()               # 文章中的图片URL
    b_pictures = scrapy.Field()                 # 文章中图片的二进制表示
    content = scrapy.Field()                    # 文章内容
    key_words = scrapy.Field()                  # 文章标签

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].iteritems():
            if attr not in ['b_pictures']:
                r[attr] = value
            else:
                r['b_pictures_len'] = len(value)
        return json.dumps(r, sort_keys=True, indent=4, separators=(',', ': '))

    def __str__(self):
        return ""
