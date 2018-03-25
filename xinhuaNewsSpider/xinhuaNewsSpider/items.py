# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item
from pprint import pformat


class NewsItem(Item):
    url = Field()
    key_words = Field()
    path_text = Field()
    path_href = Field()
    title = Field()
    date_time = Field()
    source = Field()
    content = Field()
    picture_urls = Field()
    # video_urls = Field()
    picture_texts = Field()
    editor = Field()
    author = Field()
    b_pictures = Field()

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

class CommentItem(Item):
    pass
