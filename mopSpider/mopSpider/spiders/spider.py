#! /usr/bin python3
# -*- coding: utf-8 -*-
import json
import urllib

from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from mopSpider.items import FansItem
from mopSpider.spiders.author import get_author_item
from mopSpider.spiders.comment import get_comment_item
from mopSpider.spiders.fans import get_fans_item
from mopSpider.spiders.post import get_post_item


class MopSpider(CrawlSpider):
    name = 'mop'

    allowed_domains = ['mop.com']

    start_urls = ['http://dzh.mop.com/']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/\d+.html',
            '/nofresh/\d+',
            'mop\.com/\d+'
        ),
        allow_domains=(
            'dzh.mop.com'
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
            '/space/\d+/profile',
        ),
        allow_domains=(
            'hi.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    author_page_extract = LxmlLinkExtractor(
        allow=(
            '/space/\d+',
        ),
        allow_domains=(
            'hi.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    fans_extract = LxmlLinkExtractor(
        allow=(
            '/space/\d+/fans',
        ),
        allow_domains=(
            'hi.mop.com'
        ),
        # deny=(
        #
        # ),
        # deny_domains=(
        #
        # )
    )

    friends_extract = LxmlLinkExtractor(
        allow=(
            '/space/\d+/follow',
        ),
        allow_domains=(
            'hi.mop.com'
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
            'dzh.mop.com'
        ),
        # deny=(
        #     '/print.html'
        # ),
        # deny_domains=(
        #     'q.blog.sina.com.cn'
        # )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(fans_extract, follow=True, callback='parse_fans'),
        Rule(friends_extract, follow=True, callback='parse_friends'),
        Rule(author_page_extract, follow=True),
        Rule(post_extract, follow=True, callback='parse_post'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True),
    )

    a_p_count = 0
    a_count = 0
    p_count = 0
    f_count = 0

    # def parse_page(self, response):
    #     self.a_p_count += 1
    #     print('author page: ', self.a_p_count, '  ', response.url)

    def parse_author(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        author_item = get_author_item(response)
        author_id = author_item['author_id']

        data_param = 'data=%7B"header"%3A%7B%7D%2C"req"%3A%7B"User%2FSubCount"%3A%7B"uid"%3A"' + \
                     author_id + '"%7D%2C"User%2FSnsCount"%3A%7B"uid"%3A"' + author_id + '"%7D%7D%7D'

        data_url = 'http://hi.mop.com/ajax/get?' + data_param

        yield Request(
            url=data_url,
            callback=self.parse_author_data,
            method='POST',
            meta={
                'author_item': author_item
            },
            priority=10,
        )

    def parse_author_data(self, response):
        author_item = response.meta['author_item']
        data_json = response.text
        try:
            json_obj = json.loads(data_json)
            if json_obj:
                friends_num = json_obj['resp']['User/SnsCount']['retObj']['follow']
                author_item['friends_num'] = friends_num

                fans_num = json_obj['resp']['User/SnsCount']['retObj']['fans']
                author_item['fans_num'] = fans_num

                post_num = json_obj['resp']['User/SubCount']['retObj']['subject']
                author_item['post_num'] = post_num

                reply_num = json_obj['resp']['User/SubCount']['retObj']['reply']
                author_item['reply_num'] = reply_num
        finally:
            yield author_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item = get_post_item(response)
        post_id = post_item['post_id']

        for comment_item in get_comment_item(response, post_id):
            post_item['comment_ids'].append(comment_item['comment_id'])

            yield comment_item

        yield post_item

    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_fans(self, response):
        sel = Selector(response)
        user_id = sel.xpath('//div[@class="hpUserInfo1"]/@uid').extract_first()

        fans_list = get_fans_item(response)
        for fans_id, fans_url in fans_list:
            fans_item = FansItem()
            fans_item['fans_id'] = fans_id
            fans_item['friends_id'] = user_id

            yield fans_item
            yield Request(
                url=fans_url + '/profile',
                callback=self.parse_author
            )

    def parse_friends(self, response):
        sel = Selector(response)
        user_id = sel.xpath('//div[@class="hpUserInfo1"]/@uid').extract_first()

        friends_list = get_fans_item(response)
        for friends_id, friends_url in friends_list:
            fans_item = FansItem()
            fans_item['fans_id'] = user_id
            fans_item['friends_id'] = friends_id

            yield fans_item
            yield Request(
                url=friends_url + '/profile',
                callback=self.parse_author
            )
