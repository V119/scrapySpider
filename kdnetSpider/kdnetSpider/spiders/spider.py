#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Selector
from scrapy import Spider

from kdnetSpider.spiders.author import get_author_info, get_author_id_by_href, get_author_fans, get_author_friends
from kdnetSpider.spiders.category import get_category_list, get_last_cate_num
from kdnetSpider.spiders.comment import get_comment_info
from kdnetSpider.spiders.post import get_page_posts, get_next_page_url, get_post_info


class KDNetSpider(Spider):
    def __init__(self):
        self.cate_num_dict = get_last_cate_num()

    name = 'kdnet'

    allowed_domains = [
        'kdnet.net'
    ]

    start_urls = ['http://club.kdnet.net/index.asp']

    def parse(self, response):
        for url in self.start_urls:
            yield Request(
                url=url,
                callback=self.parse_category
            )

    def parse_category(self, response):
        """
        获取类别列表，根据当前回帖、主题数和上次爬取的回帖数、主题数做对比，判断是否需要更新某个主题
        :param response:
        :return:
        """

        for category_item in get_category_list(response):
            cate_url = category_item['url']
            if not self.cate_num_dict:
                yield Request(
                    url=cate_url,
                    callback=self.parse_post_list,
                    meta={
                        'cate_name': category_item['name']
                    }
                )

            else:
                if self.cate_num_dict[category_item['id']][0] > category_item['comment_num'] or \
                                self.cate_num_dict[category_item['id']][0] > category_item['topic_num']:
                    yield Request(
                        url=cate_url,
                        callback=self.parse_post_list,
                        meta={
                            'cate_name': category_item['name']
                        }
                    )

    def parse_post_list(self, response):
        cate_name = response.meta['cate_name']

        # 获取当前页的帖子列表
        for post_item in get_page_posts(response, cate_name):
            post_url = post_item['post_url']
            yield Request(
                url=post_url,
                callback=self.parse_post,
                meta={
                    'post_item': post_item
                }
            )

        # 获取下一页的链接
        next_page_url = get_next_page_url(response)
        if next_page_url:
            yield Request(
                url=next_page_url,
                callback=self.parse_post_list,
                meta={
                    'cate_name': cate_name
                }
            )

    def parse_post(self, response):
        post_item = response.meta['post_item']

        # 获取post信息
        get_post_info(response, post_item)

        yield post_item

        # 获取作者
        author_url = post_item['author_href']
        author_name = post_item['author']
        author_id = post_item['author_id']

        yield Request(
            url=author_url,
            callback=self.parse_author,
            meta={
                'author_name': author_name,
                'author_id': author_id
            }
        )

        # 获取评论
        for comment_item in get_comment_info(response, post_item['post_id']):
            yield comment_item

            # 获取评论用户的信息
            comment_user_href = comment_item['author_href']
            if comment_user_href:
                yield Request(
                    url=comment_user_href,
                    callback=self.parse_author,
                    meta={
                        'author_name': comment_item['author_nick'],
                        'author_id': comment_item['author_id']
                    }
                )

            # 是否有at用户，获取用户主页信息
            if 'at_href' in comment_item and comment_item['at_href']:
                yield Request(
                    url=comment_item['at_href'],
                    callback=self.parse_author,
                    meta={
                        'author_name': comment_item['at_user'],
                        'author_id': get_author_id_by_href(comment_item['at_href'])
                    }
                )

    def parse_author(self, response):
        author_name = response.meta['author_name']
        author_id = response.meta['author_id']

        author_item = get_author_info(response, author_id, author_name)

        yield author_item

        # 获取粉丝和关注
        fans_href = 'http://user.kdnet.net/follow_list.asp?t=1&userid=' + author_id

        yield Request(
            url=fans_href,
            callback=self.parse_fans,
            meta={
                'author_id': author_id
            }
        )

        friends_href = 'http://user.kdnet.net/follow_list.asp?t=0&userid=' + author_id
        yield Request(
            url=friends_href,
            callback=self.parse_friends,
            meta={
                'author_id': author_id
            }
        )

    def parse_fans(self, response):
        author_id = response.meta['author_id']

        for fans_item in get_author_fans(response, author_id):
            yield fans_item

            # 请求粉丝用户的信息
            fans_href = fans_item['_user_href']
            yield Request(
                url=fans_href,
                callback=self.parse_author,
                meta={
                    'author_name': fans_item['_user_nick'],
                    'author_id': fans_item['_user_id']
                }
            )

    def parse_friends(self, response):
        author_id = response.meta['author_id']

        for friends_item in get_author_friends(response, author_id):
            yield friends_item

            # 请求关注用户的信息
            fans_href = friends_item['_user_href']
            yield Request(
                url=fans_href,
                callback=self.parse_author,
                meta={
                    'author_name': friends_item['_user_nick'],
                    'author_id': friends_item['_user_id']
                }
            )
