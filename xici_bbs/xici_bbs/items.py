# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    url = scrapy.Field()
    parse_time = scrapy.Field()

    post_id = scrapy.Field()

    key_words = scrapy.Field()

    title = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    date_time = scrapy.Field()

    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    comment_ids = scrapy.Field()


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    parse_time = scrapy.Field()
    post_id = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    date_time = scrapy.Field()
    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    floor = scrapy.Field()


class AuthorItem(scrapy.Item):
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    parse_time = scrapy.Field()

    register_time = scrapy.Field()
