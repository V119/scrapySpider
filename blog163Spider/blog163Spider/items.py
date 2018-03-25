# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    id = scrapy.Field()                                 # 文章id
    post_url = scrapy.Field()                           # 文章url
    title = scrapy.Field()                              # 标题
    date_time = scrapy.Field()                          # 时间
    category = scrapy.Field()                               # 标签
    key_words = scrapy.Field()

    author_id = scrapy.Field()                          # 作者id
    author_name = scrapy.Field()                        # 作者名
    author_href = scrapy.Field()                        # 作者url

    content = scrapy.Field()                            # post内容

    picture_hrefs = scrapy.Field()                      # 文章中图片链接
    picture_path = scrapy.Field()                       # 图片的本地存储路径

    hrefs_in_post = scrapy.Field()                      # 文章中的URL

    read_num = scrapy.Field()                           # 文章阅读量
    comment_num = scrapy.Field()                        # 文章的评论数


class AuthorItem(scrapy.Item):
    id = scrapy.Field()                                 # 用户主页url的md5码
    url = scrapy.Field()                                # 个人页面url

    nick = scrapy.Field()                               # 昵称
    real_name = scrapy.Field()                          # 真实姓名
    sex = scrapy.Field()                                # 性别
    birthday = scrapy.Field()                           # 生日
    hometown = scrapy.Field()                           # 故乡
    apartment = scrapy.Field()                          # 现居地
    introduce = scrapy.Field()                          # 自我介绍
    wish = scrapy.Field()                               # 近期心愿
    circle = scrapy.Field()                             # 加入的圈子

    level = scrapy.Field()                              # 等级
    point = scrapy.Field()                              # 积分
    register_time = scrapy.Field()                      # 注册时间
    update_time = scrapy.Field()                        # 最近更新时间
    last_login = scrapy.Field()                         # 最后登陆时间

    information = scrapy.Field()                        # 个人信息
    experience = scrapy.Field()                         # 个人经历
    contact = scrapy.Field()                            # 联系方式


class CommentItem(scrapy.Item):
    post_id = scrapy.Field()
    comment_id = scrapy.Field()

    author_id = scrapy.Field()
    author_name = scrapy.Field()
    author_href = scrapy.Field()

    content = scrapy.Field()
    date_time = scrapy.Field()
    replay_comment_id = scrapy.Field()
    child_comment_ids = scrapy.Field()
    parse_time = scrapy.Field()




