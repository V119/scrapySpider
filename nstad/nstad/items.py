# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class NstadItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
class NewsItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()


class PolicyItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()


class ResultItem(scrapy.Item):
    pid = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    key_words = scrapy.Field()
    desc = scrapy.Field()
