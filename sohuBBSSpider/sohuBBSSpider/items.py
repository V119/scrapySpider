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

    content = scrapy.Field()
    date_time = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    read_num = scrapy.Field()
    reply_num = scrapy.Field()

    comment_ids = scrapy.Field()

    parse_time = scrapy.Field()


class CommentItem(scrapy.Item):
    post_id = scrapy.Field()

    floor = scrapy.Field()

    comment_id = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    content = scrapy.Field()
    date_time = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    quote_floor = scrapy.Field()

    parse_time = scrapy.Field()


class AuthorItem(scrapy.Item):
    author_id = scrapy.Field()
    nick_name = scrapy.Field()

    sex = scrapy.Field()
    level = scrapy.Field()
    title = scrapy.Field()
    introduction = scrapy.Field()

    duty = scrapy.Field()
    post_num = scrapy.Field()
    elite_num = scrapy.Field()
    point = scrapy.Field()
    birthday = scrapy.Field()
    online_time = scrapy.Field()
    reputation = scrapy.Field()
    last_login = scrapy.Field()
    login_num = scrapy.Field()

    sport = scrapy.Field()
    movie = scrapy.Field()
    music = scrapy.Field()
    food = scrapy.Field()
    book = scrapy.Field()
    person = scrapy.Field()

    education = scrapy.Field()
    profession = scrapy.Field()

    friends_num = scrapy.Field()
    fans_num = scrapy.Field()

    parse_time = scrapy.Field()


class FansItem(scrapy.Item):
    fans = scrapy.Field()
    follow = scrapy.Field()
