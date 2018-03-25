#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from sinaBlogSpider.spiders.author import get_author_info
from sinaBlogSpider.spiders.comment import get_comment_ajax, get_comment_info
from sinaBlogSpider.spiders.post import get_post_item, get_num_div_info


class SinaBlogSpider(CrawlSpider):
    name = 'sina_blog'

    allowed_domains = ['blog.sina.com.cn']

    start_urls = ['http://blog.sina.com.cn/']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/s/blog_',
        ),
        allow_domains=(
            'blog.sina.com.cn'
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
            '/s/profile_',
        ),
        allow_domains=(
            'blog.sina.com.cn'
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
            'blog.sina.com.cn'
        ),
        deny=(
            '/print.html'
        ),
        deny_domains=(
            'q.blog.sina.com.cn'
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
        author_item = get_author_info(response)

        yield author_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item = get_post_item(response)

        post_num_url = 'http://comet.blog.sina.com.cn/api?maintype=num&uid=' \
                       + post_item['post_id'][:8] + '&aids=' + post_item['post_id'][-6:]

        yield Request(
            url=post_num_url,
            callback=self.parse_post_num_part,
            meta={
                'post_item': post_item
            }
        )

    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_comment(self, response):
        """
        获取评论信息
        :param response:
        :return:
        """
        post_id = response.meta['post_id']
        page = response.meta['page']
        comment_list, comment_num = get_comment_info(response, post_id)
        for comment_item in comment_list:
            yield comment_item

        if comment_num.isdigit() and int(comment_num) >= 50:
            page += 1
            comment_url = get_comment_ajax(post_id, page)

            yield Request(
                url=comment_url,
                callback=self.parse_comment,
                meta={
                    'post_id': post_id,
                    'page': 1
                }
            )

    def parse_post_num_part(self, response):
        post_item = response.meta['post_item']
        get_num_div_info(response, post_item)

        yield post_item

        post_id = post_item['post_id']
        comment_url = get_comment_ajax(post_id)
        yield Request(
            url=comment_url,
            callback=self.parse_comment,
            meta={
                'post_id': post_id,
                'page': 1
            }
        )
