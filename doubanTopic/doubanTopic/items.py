# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    id = scrapy.Field()                     # id
    title = scrapy.Field()                  # 标题
    date_time = scrapy.Field()              # 发表时间
    reply_num = scrapy.Field()              # 回应的数量
    topic = scrapy.Field()                  # 所属主题
    article = scrapy.Field()                # 文章内容
    article_url = scrapy.Field()            # 文章内容链接
    author_name = scrapy.Field()            # 作者ID
    # author_sign = scrapy.Field()            # 签名
    like_num = scrapy.Field()               # 喜欢数
    recommend_num = scrapy.Field()          # 推荐数
    keywords = scrapy.Field()


class CommentItem(scrapy.Item):
    id = scrapy.Field()
    post_id = scrapy.Field()
    author_name = scrapy.Field()
    date_time = scrapy.Field()
    comment = scrapy.Field()
    prise_num = scrapy.Field()


