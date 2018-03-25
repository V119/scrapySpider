# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    post_id = scrapy.Field()
    url = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()

    title = scrapy.Field()
    key_words = scrapy.Field()
    tags = scrapy.Field()
    date_time = scrapy.Field()
    create_time = scrapy.Field()

    content = scrapy.Field()

    picture_href = scrapy.Field()
    picture_path = scrapy.Field()

    category = scrapy.Field()

    comment_num = scrapy.Field()

    comment_ids = scrapy.Field()


class AuthorItem(scrapy.Item):
    url = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()

    level = scrapy.Field()
    friends_num = scrapy.Field()
    fans_num = scrapy.Field()

    point = scrapy.Field()
    login_num = scrapy.Field()

    register_date = scrapy.Field()

    location = scrapy.Field()


class CommentItem(scrapy.Item):
    post_id = scrapy.Field()
    comment_id = scrapy.Field()

    author_name = scrapy.Field()
    author_href = scrapy.Field()
    author_id = scrapy.Field()

    content = scrapy.Field()
    date_time = scrapy.Field()


class FansItem(scrapy.Item):
    fans_id = scrapy.Field()
    friends_id = scrapy.Field()

