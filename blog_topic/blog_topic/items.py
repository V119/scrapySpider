# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from pprint import pformat


class UserInfoItem(scrapy.Item):
    #
    url = scrapy.Field()  # 用户信息URL
    parse_time = scrapy.Field()
    user_id = scrapy.Field()
    page_id = scrapy.Field()

    # 基本信
    head_img_url = scrapy.Field()
    nick_name = scrapy.Field()
    real_name = scrapy.Field()
    location = scrapy.Field()
    sex = scrapy.Field()
    sexual_orientation = scrapy.Field()
    Relationship_status = scrapy.Field()
    birthday = scrapy.Field()
    blog_address = scrapy.Field()
    personal_url = scrapy.Field()
    description = scrapy.Field()
    register_date = scrapy.Field()
    mail = scrapy.Field()
    qq = scrapy.Field()
    blood_type = scrapy.Field()

    # 公司信息,list[dict]类型数据
    company = scrapy.Field()

    # 教育信息 list[dict]类型
    education = scrapy.Field()

    # 标签信息list
    tag = scrapy.Field()

    # 关注数量
    friends_num = scrapy.Field()

    # 粉丝数量
    fans_num = scrapy.Field()

    # 博客数量
    blog_num = scrapy.Field()

    # 等级
    rank = scrapy.Field()

    # 加V类型
    is_v = scrapy.Field()

    # 图片的二进制表示
    b_head_img_url = scrapy.Field()

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)

    def __str__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)


class FansItem(scrapy.Item):
    fans_id = scrapy.Field()
    follow_id = scrapy.Field()


class BlogItem(scrapy.Item):
    praise_time = scrapy.Field()  # 爬取微博的时间

    mid = scrapy.Field()  # 微博id
    user_href = scrapy.Field()  # 用户主页ID
    user_id = scrapy.Field()  # 用户ID
    is_forward = scrapy.Field()  # 是否是转发
    o_mid = scrapy.Field()  # 原微博ID
    o_user_id = scrapy.Field()  # 原微博用户ID
    # head_img_url = scrapy.Field()               # 用户头像
    blog_info = scrapy.Field()  # 微博内容
    date_time = scrapy.Field()  # 发微博时间
    exact_time = scrapy.Field()  # 精确的时间
    data_from = scrapy.Field()  # 来自xxx
    at_list = scrapy.Field()  # 用户@的列表
    at_url_list = scrapy.Field()
    topic_list = scrapy.Field()  # 话题列表
    topic_url_list = scrapy.Field()
    picture_url = scrapy.Field()  # 用户图片URL

    # 头条文章
    article_url = scrapy.Field()  # 文章的url
    article_date_time = scrapy.Field()  # 文章的时间
    article_title = scrapy.Field()  # 文章标题
    article_preface = scrapy.Field()  # 文章导语
    article_content = scrapy.Field()  # 文章正文
    article_pic_url_desc = scrapy.Field()  # 文章图片url
    article_media_url = scrapy.Field()  # 文章中多媒体链接
    article_read_num = scrapy.Field()  # 文章的阅读数

    #
    prise_num = scrapy.Field()  # 赞的数量
    comment_num = scrapy.Field()  # 评论数量
    forward_num = scrapy.Field()  # 转发数量

    # 图片的二进制表示
    b_picture_url = scrapy.Field()
    b_article_pic_url_dict = scrapy.Field()

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)

    def __str__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()  # 评论ID
    blog_id = scrapy.Field()  # 评论的博客ID
    parse_time = scrapy.Field()  # 爬虫爬取当前页面的时间
    comment_user_nick = scrapy.Field()  # 评论用户的昵称
    comment_user_id = scrapy.Field()  # 评论用户的ID
    comment_user_page = scrapy.Field()  # 评论用户的URL
    comment_date_time = scrapy.Field()  # 评论的时间
    praise_num = scrapy.Field()  # 赞的数量
    at_name_list = scrapy.Field()  # @的用户名
    at_url_list = scrapy.Field()  # @的用户url
    content = scrapy.Field()  # 评论的内容
    child_comment_ids = scrapy.Field()  # 子评论的ID
    parent_comment_id = scrapy.Field()  # 父评论的ID
    topic_url_list = scrapy.Field()  # 评论中的话题url列表
    topic_text_list = scrapy.Field()  # 评论中的话题列表
    img_url_list = scrapy.Field()

    # 图片的二进制表示
    b_img_url_list = scrapy.Field()

    def __repr__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)

    def __str__(self):
        r = {}
        for attr, value in self.__dict__['_values'].items():
            if not attr.startswith('b_'):
                r[attr] = value
            else:
                r[attr + '_len'] = len(value)
        return pformat(r)


class TopicItem(scrapy.Item):
    topic_name = scrapy.Field()
    topic_url = scrapy.Field()
    topic_orig_url = scrapy.Field()
    topic_introduction = scrapy.Field()
