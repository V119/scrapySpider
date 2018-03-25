# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from pprint import pformat

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    path_text = scrapy.Field()
    path_href = scrapy.Field()
    title = scrapy.Field()
    date_time = scrapy.Field()
    source = scrapy.Field()
    # author = scrapy.Field()
    read_num = scrapy.Field()
    comment_num = scrapy.Field()
    content = scrapy.Field()
    picture_url = scrapy.Field()
    b_pictures = scrapy.Field()

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if attr not in ['b_pictures']:
                r[attr] = value
            else:
                r['b_pictures_len'] = len(value)
        # return json.dumps(r, sort_keys=True, indent=4, separators=(',', ': '))
        return pformat(r)

    def __str__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if attr not in ['b_pictures']:
                r[attr] = value
            else:
                r['b_pictures_len'] = len(value)
        # return json.dumps(r, sort_keys=True, indent=4, separators=(',', ': '))
        return pformat(r)



