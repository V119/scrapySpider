# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    url = scrapy.Field()

    post_id = scrapy.Field()

    path_text = scrapy.Field()
    path_href = scrapy.Field()

    title = scrapy.Field()

    key_words = scrapy.Field()
    hot_words = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()

    level = scrapy.Field()
    point = scrapy.Field()

    date_time = scrapy.Field()
    read_num = scrapy.Field()
    participant_num = scrapy.Field()
    reply_num = scrapy.Field()

    _num_href = scrapy.Field()

    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    parse_time = scrapy.Field()

    comment_ids = scrapy.Field()


class AuthorItem(scrapy.Item):
    url = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()

    focuse_num = scrapy.Field()
    fans_num = scrapy.Field()

    name = scrapy.Field()
    sex = scrapy.Field()
    birthday = scrapy.Field()
    address = scrapy.Field()

    parse_time = scrapy.Field()


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()

    post_id = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()

    prise_num = scrapy.Field()
    date_time = scrapy.Field()

    floor = scrapy.Field()

    content = scrapy.Field()


