# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    url = scrapy.Field()
    post_id = scrapy.Field()

    title = scrapy.Field()

    key_words = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    date_time = scrapy.Field()

    read_num = scrapy.Field()
    reply_num = scrapy.Field()
    prise_num = scrapy.Field()

    content_href = scrapy.Field()
    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    comment_ids = scrapy.Field()

    parse_time = scrapy.Field()


class AuthorItem(scrapy.Field):
    url = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()

    post_num = scrapy.Field()
    reply_num = scrapy.Field()
    elite_num = scrapy.Field()

    level = scrapy.Field()


class CommentItem(scrapy.Field):
    comment_id = scrapy.Field()

    post_id = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    date_time = scrapy.Field()

    floor = scrapy.Field()
    prise_num = scrapy.Field()

    parent_comment_id = scrapy.Field()
