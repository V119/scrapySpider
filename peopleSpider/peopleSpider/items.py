# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import json

import scrapy


class NewsItem(scrapy.Item):
    url = scrapy.Field()                # 文章的URL
    path_text = scrapy.Field()          # 路径文字
    path_url = scrapy.Field()           # 路径url
    date_time = scrapy.Field()          # 发布日期时间
    source_text = scrapy.Field()        # 来源文本表示
    source_href = scrapy.Field()        # 来源的URL
    author = scrapy.Field()             # 作者
    editor = scrapy.Field()             # 编辑
    key_words = scrapy.Field()          # 关键字
    paper_num = scrapy.Field()          # 报纸期号
    pre_title = scrapy.Field()          # 正式标题前的标题
    title = scrapy.Field()              # 标题
    sub_title = scrapy.Field()          # 子标题
    content = scrapy.Field()            # 新闻内容
    pictures_url = scrapy.Field()        # 新闻中的图片
    b_pictures = scrapy.Field()          # 图片的二进制表示
    content_url = scrapy.Field()        # 文章中的ur

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if attr not in ['b_pictures']:
                r[attr] = value
            else:
                r['b_pictures_len'] = len(value)
        return json.dumps(r, sort_keys=True, indent=4, separators=(',', ': '))

    def __str__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if attr not in ['b_pictures']:
                r[attr] = value
            else:
                r['b_pictures_len'] = len(value)
        return json.dumps(r, sort_keys=True, indent=4, separators=(',', ': '))
