# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    user_id = scrapy.Field()                        # 用户ID
    user_name = scrapy.Field()                      # 用户名
    description = scrapy.Field()                    # 简介
    gender = scrapy.Field()                         # 性别
    follow_num = scrapy.Field()                     # 关注的人数
    fans_num = scrapy.Field()                       # 粉丝数
    verified = scrapy.Field()                       # 是否认证用户
    verified_reason = scrapy.Field()                # 认证原因
    verified_type = scrapy.Field()                  # 认证类型
    verified_type_ext = scrapy.Field()

    blog_id = scrapy.Field()                        # 博客ID
    blog = scrapy.Field()                           # 博客内容
    page_url = scrapy.Field()                       # page的URL
    page_type = scrapy.Field()                      # page的类型
    date = scrapy.Field()                           # 日期
    forward_num = scrapy.Field()                    # 转发数
    comment_num = scrapy.Field()                    # 评论数
    prise_num = scrapy.Field()                      # 点赞数


class CommentItem(scrapy.Item):
    id = scrapy.Field()
    blog_id = scrapy.Field()                        # 评论微博ID

    user_id = scrapy.Field()                        # 用户ID
    user_name = scrapy.Field()                      # 用户名
    verified = scrapy.Field()                       # 是否认证
    verified_type = scrapy.Field()                  # 认证类型
    verified_type_ext = scrapy.Field()

    comment = scrapy.Field()                        # 评论内容
    date = scrapy.Field()                           # 评论发表的日期
    comment_id = scrapy.Field()                     # 评论日期
    prise_num = scrapy.Field()                      # 点赞数
    source = scrapy.Field()                         # 来源
