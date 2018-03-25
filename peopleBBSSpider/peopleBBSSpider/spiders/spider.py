#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from peopleBBSSpider.spiders.author import get_author_item
from peopleBBSSpider.spiders.comment import get_comment_list
from peopleBBSSpider.spiders.post import get_post_item, get_post_content


class MopSpider(CrawlSpider):
    name = 'people_bbs'

    start_urls = ['http://bbs1.people.com.cn/']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/post/',
        ),
        allow_domains=(
            'bbs1.people.com.cn'
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
            '/userInfo\.do\?',
        ),
        allow_domains=(
            'bbs1.people.com.cn',
        ),
        deny=(
            '/userInfo\.do\?action=thread',
            '/userInfo\.do\?action=follow',
            '/userInfo\.do\?action=jinghua',
            '/userInfo\.do\?orderBy=',
        ),
        # deny_domains=(
        #
        # )
    )

    follow_extract = LxmlLinkExtractor(
        # allow=(
        #     '/s/[0-9]+',
        # ),
        allow_domains=(
            'bbs1.people.com.cn',
        ),
        deny=(
            '/userInfo\.do\?action=thread',
            '/userInfo\.do\?action=follow',
            '/userInfo\.do\?action=jinghua',
            '/userInfo\.do\?orderBy=',
        ),
        # deny_domains=(
        #     'q.blog.sina.com.cn'
        # )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(post_extract, follow=True, callback='parse_post'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True, process_request=),
    )
    #
    # a_count = 0
    # p_count = 0
    # f_count = 0

    def parse_author(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)

        author_item = get_author_item(response)

        if author_item:

            yield author_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)

        post_item = get_post_item(response)

        content_href = post_item['content_href']

        if content_href:
            yield Request(
                url=content_href,
                callback=self.parse_content,
                meta={
                    'post_item': post_item
                }
            )
        else:
            pass

    def parse_content(self, response):
        post_item = response.meta['post_item']

        content, picture_hrefs = get_post_content(response)

        post_item['content'] = content
        post_item['picture_hrefs'] = picture_hrefs

        for comment_item in get_comment_list(response):
            post_item['comment_ids'].append(comment_item['comment_id'])

            yield comment_item

        yield post_item
