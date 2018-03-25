# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    post_id = scrapy.Field()

    url = scrapy.Field()

    path_href = scrapy.Field()
    path_text = scrapy.Field()

    title = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_url = scrapy.Field()

    date_time = scrapy.Field()

    read_num = scrapy.Field()
    comment_num = scrapy.Field()
    like_num = scrapy.Field()

    detail_href = scrapy.Field()
    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    parse_time = scrapy.Field()

    comment_ids = scrapy.Field()


class AuthorItem(scrapy.Item):
    url = scrapy.Field()

    author_id = scrapy.Field()
    author_href = scrapy.Field()
    author_name = scrapy.Field()

    post_num = scrapy.Field()
    level = scrapy.Field()

    login_num = scrapy.Field()
    register_time = scrapy.Field()

    parse_time = scrapy.Field()


class CommentItem(scrapy.Item):
    post_id = scrapy.Field()
    comment_id = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    floor = scrapy.Field()

    date_time = scrapy.Field()
    content = scrapy.Field()

    refer = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    prise_num = scrapy.Field()

    parse_time = scrapy.Field()


class FansItem(scrapy.Item):
    fans_id = scrapy.Field()
    friends_id = scrapy.Field()

