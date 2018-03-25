# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AuthorItem(scrapy.Item):
    url = scrapy.Field()                    # 用户主页URL
    author_id = scrapy.Field()                # 用户ID
    nick = scrapy.Field()                   # 用户名
    level = scrapy.Field()                  # 等级
    influence = scrapy.Field()              # 影响力
    hits = scrapy.Field()                   # 点击量
    post_num = scrapy.Field()               # 主帖数
    fans_num = scrapy.Field()               # 粉丝数
    friends_num = scrapy.Field()            # 关注数
    register_time = scrapy.Field()          # 注册时间
    login_num = scrapy.Field()              # 登陆次数
    parse_time = scrapy.Field()             # 爬取的当前时间


class PostItem(scrapy.Item):
    # post_type = scrapy.Field()              # 话题类型（原创、转贴、灌水）
    post_id = scrapy.Field()                # 帖子ID
    post_status = scrapy.Field()            # 帖子状态
    post_url = scrapy.Field()               # 帖子的URL
    title = scrapy.Field()                  # 帖子题目
    author = scrapy.Field()                 # 帖子作者
    author_href = scrapy.Field()            # 帖子作者的主页
    author_id = scrapy.Field()              # 作者主页ID
    post_time = scrapy.Field()              # 发布时间
    category = scrapy.Field()               # 类别
    hits = scrapy.Field()                   # 点击量
    comment_num = scrapy.Field()            # 回复数
    at_user = scrapy.Field()                # @的用户名
    at_href = scrapy.Field()                # @的用户主页
    pictures_href = scrapy.Field()          # post图片URL
    pictures_local_uri = scrapy.Field()     # post图片的本地路径
    content = scrapy.Field()                # 文本内容

    parse_time = scrapy.Field()             # 爬取的当前时间

    _last_update = scrapy.Field()           # 文章最后更新时间


class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()             # 评论ID
    author_href = scrapy.Field()            # 用户主页链接
    author_nick = scrapy.Field()            # 评论人的昵称
    author_id = scrapy.Field()              # 评论的用户ID
    post_id = scrapy.Field()                # 评论的文章ID
    floor_num = scrapy.Field()              # 楼层数
    date_time = scrapy.Field()              # 评论的时间日期
    content = scrapy.Field()                # 内容
    at_user = scrapy.Field()                # @的用户名
    at_href = scrapy.Field()                # @的用户主页
    pictures_href = scrapy.Field()          # post图片URL
    pictures_local_uri = scrapy.Field()     # post图片的本地路径
    quote_comment_id = scrapy.Field()       # 引用的评论ID
    parse_time = scrapy.Field()             # 爬取的当前时间


class FansItem(scrapy.Item):
    fans = scrapy.Field()                   # 粉丝
    friends = scrapy.Field()                # 关注者

    _user_id = scrapy.Field()               # 获得的用户关注或粉丝的ID
    _user_nick = scrapy.Field()             # 获得的用户关注或粉丝的用户名
    _user_href = scrapy.Field()             # 获得的用户关注或粉丝的主页链接


class CategoryItem(scrapy.Field):
    id = scrapy.Field()                     # 板块的ID
    name = scrapy.Field()                   # 板块名
    url = scrapy.Field()                    # 板块的URL
    today_num = scrapy.Field()              # 今日帖子数
    comment_num = scrapy.Field()            # 回帖数
    topic_num = scrapy.Field()              # 主题数
    parse_time = scrapy.Field()             # 爬取时间



