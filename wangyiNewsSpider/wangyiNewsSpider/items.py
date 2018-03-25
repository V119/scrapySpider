# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    url = scrapy.Field()
    spider_time = scrapy.Field()
    keywords = scrapy.Field()
    description = scrapy.Field()
    author = scrapy.Field()
    path_text = scrapy.Field()
    path_href = scrapy.Field()
    title = scrapy.Field()
    date_time = scrapy.Field()
    source_text = scrapy.Field()
    source_href = scrapy.Field()
    content = scrapy.Field()
    picture_urls = scrapy.Field()
    editor = scrapy.Field()

    comment_num = scrapy.Field()

    b_pictures = scrapy.Field()
