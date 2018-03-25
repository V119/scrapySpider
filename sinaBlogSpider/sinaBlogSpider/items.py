# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorItem(scrapy.Item):
    url = scrapy.Field()                                # 网页链接

    author_id = scrapy.Field()                          # 作者ID
    author_name = scrapy.Field()                        # 作者名

    picture_head_url = scrapy.Field()                   # 头像URL
    picture_head_local = scrapy.Field()                 # 头像的本地存储路径

    level = scrapy.Field()                              # 等级
    point = scrapy.Field()                              # 积分
    visit_num = scrapy.Field()                          # 访问次数
    popularity = scrapy.Field()                         # 关注人气
    get_golden = scrapy.Field()                         # 获赠金笔数
    give_golden = scrapy.Field()                        # 赠出金笔数

    info = scrapy.Field()                               # 基本信息
    experience = scrapy.Field()                         # 个人经历
    introduction = scrapy.Field()                       # 个人简介
    certification = scrapy.Field()                      # 认证类型


class PostItem(scrapy.Item):
    url = scrapy.Field()                                # url

    post_id = scrapy.Field()                            # 文章的ID

    author_id = scrapy.Field()                          # 作者ID
    author_name = scrapy.Field()                        # 作者名
    author_href = scrapy.Field()                        # 作者主页链接

    title = scrapy.Field()                              # 标题
    date_time = scrapy.Field()                          # 时间
    key_words = scrapy.Field()                          # 关键字
    tags = scrapy.Field()                               # 标签

    content = scrapy.Field()
    picture_urls = scrapy.Field()                       # 页面中图片URL
    picture_local_path = scrapy.Field()                 # 图片在本地存储路径
    url_in_content = scrapy.Field()                     # 博客正文中的图片

    enjoy_num = scrapy.Field()                          # 喜欢的数量
    get_golden_num = scrapy.Field()                     # 获得的金笔
    read_num = scrapy.Field()                           # 阅读数量
    comment_num = scrapy.Field()                        # 评论数量
    collect_num = scrapy.Field()                        # 收藏数量
    forward_num = scrapy.Field()                        # 转载的数量


class CommentItem(scrapy.Item):
    post_id = scrapy.Field()                            # 评论的文章ID

    comment_id = scrapy.Field()                         # 评论的ID

    author_id = scrapy.Field()                          # 作者ID
    author_name = scrapy.Field()                        # 作者名
    author_href = scrapy.Field()                        # 作者主页链接

    content = scrapy.Field()                            # 评论内容
    date_time = scrapy.Field()                          # 日期时间
    replay_num = scrapy.Field()                         # 回复该条评论的数量




