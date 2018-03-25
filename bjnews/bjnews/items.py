# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BjnewsItem(scrapy.Item):
    id = scrapy.Field()
    date = scrapy.Field()
    page_info = scrapy.Field()
    first_title = scrapy.Field()
    second_title = scrapy.Field()
    content = scrapy.Field()
    parse_time = scrapy.Field()
