#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from tianyaBBSSpider.items import FansItem
from tianyaBBSSpider.spiders.author import get_author_item
from tianyaBBSSpider.spiders.comment import get_comment_item, get_comment_next_page
from tianyaBBSSpider.spiders.fans import get_fans_url, get_friends_url, get_fans_user_id_list
from tianyaBBSSpider.spiders.post import get_post_item


class MopSpider(CrawlSpider):
    name = 'tianya_bbs'

    start_urls = ['http://blog.tianya.cn']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/post-\d+-\d+-1.shtml',
        ),
        allow_domains=(
            'blog.tianya.cn'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    author_extract = LxmlLinkExtractor(
        allow=(
            '/\d+$',
        ),
        allow_domains=(
            'www.tianya.cn'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    follow_extract = LxmlLinkExtractor(
        # allow=(
        #     '/s/[0-9]+',
        # ),
        allow_domains=(
            'blog.tianya.cn',
        ),
        deny=(
            '/webadmin/blog_setpost.jsp',
            '/webadmin/blog_changepost.jsp',
        ),
        # deny_domains=(
        #     'q.blog.sina.com.cn'
        # )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(post_extract, follow=True, callback='parse_post'),
        Rule(follow_extract, follow=True, callback='parse_follow'),
        # Rule(follow_extract, follow=True),
    )

    a_count = 0
    p_count = 0
    f_count = 0

    def parse_author(self, response):
        # print(response.text)
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        author_item = get_author_item(response)

        author_id = author_item['author_id']
        if author_id:
            fans_url = get_fans_url(author_id, '1')
            yield Request(
                url=fans_url,
                callback=self.parse_fans,
                meta={
                    'author_id': author_id,
                    'page_num': 1,
                },
            )

            friends_url = get_friends_url(author_id, '1')
            yield Request(
                url=friends_url,
                callback=self.parse_friends,
                meta={
                    'author_id': author_id,
                    'page_num': 1,
                },
            )

        yield author_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item = get_post_item(response)

        for item_or_request in self.__get_post_comment(response, post_item):
            yield item_or_request

    #
    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_fans(self, response):
        author_id = response.meta['author_id']
        page_num = response.meta['page_num']
        fans_id_list = get_fans_user_id_list(response)
        for fans_id in fans_id_list:
            fans_item = FansItem()
            fans_item['fans_id'] = fans_id
            fans_item['friends_id'] = author_id

            yield fans_item

            fans_href = 'http://www.tianya.cn/' + str(fans_id)
            yield Request(
                url=fans_href,
                callback=self.parse_author,
            )
        if fans_id_list and len(fans_id_list) >= 28 and page_num < 5:
            yield Request(
                url=get_fans_url(author_id, str(page_num + 1)),
                callback=self.parse_fans,
                meta={
                    'author_id': author_id,
                    'page_num': page_num + 1
                },
            )

    def parse_friends(self, response):
        author_id = response.meta['author_id']
        page_num = response.meta['page_num']
        friends_id_list = get_fans_user_id_list(response)
        for friends_id in friends_id_list:
            fans_item = FansItem()
            fans_item['friends_id'] = friends_id
            fans_item['fans_id'] = author_id

            yield fans_item

            friends_href = 'http://www.tianya.cn/' + str(friends_id)
            yield Request(
                url=friends_href,
                callback=self.parse_author,
            )

        if friends_id_list and len(friends_id_list) >= 28 and page_num < 5:
            yield Request(
                url=get_fans_url(author_id, str(page_num + 1)),
                callback=self.parse_friends,
                meta={
                    'author_id': author_id,
                    'page_num': page_num + 1
                },
            )

    def parse_next_page_comment(self, response):
        post_item = response.meta['post_item']
        for item_or_request in self.__get_post_comment(response, post_item):
            yield item_or_request

    def __get_post_comment(self, response, post_item):
        for comment_item in get_comment_item(response):
            comment_item['post_id'] = post_item['post_id']
            post_item['comment_ids'].append(comment_item['comment_id'])

            yield comment_item

            if comment_item['comment_id']:
                yield Request(
                    url='http://blog.tianya.cn/' + comment_item['comment_id'],
                    callback=self.parse_author,
                )

        comment_next_page_url = get_comment_next_page(response)
        if comment_next_page_url:
            yield Request(
                url=comment_next_page_url,
                callback=self.parse_next_page_comment,
                meta={
                    'post_item': post_item,
                }
            )
        else:
            yield post_item
