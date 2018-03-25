# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    url = scrapy.Field()

    post_id = scrapy.Field()

    group_name = scrapy.Field()
    group_href = scrapy.Field()
    group_id = scrapy.Field()

    author_name = scrapy.Field()
    author_href = scrapy.Field()
    author_id = scrapy.Field()

    title = scrapy.Field()
    date_time = scrapy.Field()

    content = scrapy.Field()

    picture_hrefs = scrapy.Field()
    picture_path = scrapy.Field()

    recommend_num = scrapy.Field()
    like_num = scrapy.Field()

    comment_ids = scrapy.Field()


class GroupItem(scrapy.Item):
    url = scrapy.Field()

    group_id = scrapy.Field()
    group_name = scrapy.Field()

    create_time = scrapy.Field()

    leader_name = scrapy.Field()
    leader_href = scrapy.Field()
    # leader_id = scrapy.Field()

    content = scrapy.Field()

    group_tags = scrapy.Field()


class CommentItem(scrapy.Item):
    url = scrapy.Field()

    comment_id = scrapy.Field()

    post_id = scrapy.Field()

    author_name = scrapy.Field()
    author_href = scrapy.Field()
    author_id = scrapy.Field()

    content = scrapy.Field()

    pub_time = scrapy.Field()
    prise_num = scrapy.Field()

    quote_content = scrapy.Field()
    quote_author_name = scrapy.Field()
    quote_author_href = scrapy.Field()


class AuthorItem(scrapy.Item):
    url = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()

    signature = scrapy.Field()

    location = scrapy.Field()
    join_time = scrapy.Field()

    logoff_time = scrapy.Field()

    introduction = scrapy.Field()


class FansItem(scrapy.Item):
    fans_id = scrapy.Field()
    friends_id = scrapy.Field()
