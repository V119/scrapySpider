# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PeoplePaperItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    date = scrapy.Field()
    page_info = scrapy.Field()
    first_title = scrapy.Field()
    second_title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    parse_time = scrapy.Field()
