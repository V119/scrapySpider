#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from xici_bbs.spiders.author import get_author_item
from xici_bbs.spiders.comment import get_comment_list, get_comment_next_page
from xici_bbs.spiders.post import get_post_item


class XiciSpider(CrawlSpider):
    name = 'xici'

    start_urls = ['http://www.xici.net']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/d\d+.htm',
        ),
        allow_domains=(
            'xici.net'
        ),
        # deny=(
        #
        # ),
        deny_domains=(
            'account.xici.net',
        )
    )

    author_extract = LxmlLinkExtractor(
        allow=(
            '/u\d+$',
            '/u\d+/$',
        ),
        allow_domains=(
            'xici.net',
        ),
        # deny=(
        #
        # ),
        deny_domains=(
            'account.xici.net',
        )
    )

    follow_extract = LxmlLinkExtractor(
        # allow=(
        #     '/s/[0-9]+',
        # ),
        allow_domains=(
            'xici.net',
        ),
        deny=(
            '/help/',
        ),
        deny_domains=(
            'account.xici.net',
            # 'life.xici.net',
        )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(post_extract, follow=True, callback='parse_post'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True),
    )

    # a_count = 0
    # p_count = 0
    # f_count = 0

    def parse_author(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        author_item = get_author_item(response)

        yield author_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item = get_post_item(response)

        for item_or_request in self.parse_comment(response, post_item):
            yield item_or_request

    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_comment(self, response, post_item=None):
        if not post_item:
            post_item = response.meta['post_item']

        for comment_item in get_comment_list(response):
            post_item['comment_ids'].append(comment_item['comment_id'])

            yield comment_item

        comment_next_page = get_comment_next_page(response)
        if comment_next_page:
            yield Request(
                url=comment_next_page,
                callback=self.parse_comment,
                meta={
                    'post_item': post_item,
                }
            )

        else:
            yield post_item

