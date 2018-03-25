#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from newsBBSSpider.items import FansItem
from newsBBSSpider.spiders.author import get_author_item, gen_author_id
from newsBBSSpider.spiders.comment import get_comment_list, get_next_page_url
from newsBBSSpider.spiders.fans import get_fans_list, get_total_page_num, get_fans_next_page
from newsBBSSpider.spiders.post import get_post_item


class NewsBBSSpider(CrawlSpider):
    name = 'news_bbs'

    start_urls = ['http://forum.home.news.cn']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/detail/\d+/1.html',
        ),
        allow_domains=(
            'forum.home.news.cn'
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
            '/space/userspace\.do\?',
        ),
        allow_domains=(
            'forum.home.news.cn',
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
            '/portal/attentionlist',
        ),
        allow_domains=(
            'home.news.cn',
        ),
    )

    friends_extract = LxmlLinkExtractor(
        allow=(
            '/portal/followlist',
        ),
        allow_domains=(
            'home.news.cn',
        ),
    )

    follow_extract = LxmlLinkExtractor(
        # allow=(
        #     '/s/[0-9]+',
        # ),
        allow_domains=(
            'forum.home.news.cn',
            'home.news.cn',
        ),
        deny=(
            '/detail/\d+/\d+.html',
            '/blog/',
            '/bookmark/',
            '/portal/img/',
            '/portal/video/',
            '/portal/message',
            '/portal/mblog',
            '/portal/user',
        ),
        deny_domains=(
            'login.home.news.cn',
            't.home.news.cn',
            'blog.home.news.cn',
        )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(post_extract, follow=True, callback='parse_post'),
        Rule(fans_extract, follow=True, callback='parse_fans'),
        Rule(friends_extract, follow=True, callback='parse_friends'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True),
    )

    a_count = 0
    p_count = 0
    f_count = 0
    fans_count = 0
    friends_count = 0

    def parse_author(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        author_item = get_author_item(response)

        yield author_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item = get_post_item(response)

        for comment_request in self.get_comment_list(response, post_item):
            yield comment_request

    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_fans(self, response):
        page_num = response.meta.get('page_num')
        total_page = response.meta.get('total_page')
        if not page_num:
            page_num = 0
        if not total_page:
            total_page = get_total_page_num(response)

        url = response.url
        user_id = gen_author_id(url)

        if page_num > 0:
            for fans_id in get_fans_list(response):
                fans_item = FansItem()
                fans_item['fans_id'] = fans_id
                fans_item['friends_id'] = user_id

                yield fans_item

        if page_num < total_page:
            next_page_url = get_fans_next_page(response, page_num + 1, 0)

            yield Request(
                url=next_page_url,
                callback=self.parse_fans,
                meta={
                    'page_num': page_num + 1,
                    'total_page': total_page,
                }
            )

    def parse_friends(self, response):
        # self.friends_count += 1
        # print('friends: ', self.friends_count, '  ', response.url)
        page_num = response.meta.get('page_num')
        total_page = response.meta.get('total_page')
        if not page_num:
            page_num = 0
        if not total_page:
            total_page = get_total_page_num(response)
        url = response.url
        user_id = gen_author_id(url)
        if page_num > 0:
            for friends_id in get_fans_list(response):
                friends_item = FansItem()
                friends_item['fans_id'] = user_id
                friends_item['friends_id'] = friends_id

                yield friends_item

        if page_num < total_page:
            next_page_url = get_fans_next_page(response, page_num + 1, 1)

            yield Request(
                url=next_page_url,
                callback=self.parse_friends,
                meta={
                    'page_num': page_num + 1,
                    'total_page': total_page,
                }
            )

    def get_comment_list(self, response, post_item=None):
        if not post_item:
            post_item = response.meta['post_item']

        for comment_item in get_comment_list(response):
            post_item['comment_ids'].append(comment_item['comment_id'])

            yield comment_item

        next_page_href = get_next_page_url(response)

        if not next_page_href:
            if post_item['detail_href']:
                yield Request(
                    url=post_item['detail_href'],
                    callback=self.parse_detail,
                    meta={
                        'post_item': post_item,
                    }
                )
            else:
                yield post_item
        else:
            yield Request(
                url=next_page_href,
                callback=self.get_comment_list,
                meta={
                    'post_item': post_item,
                }
            )

    def parse_detail(self, response):
        sel = Selector(response)
        post_item = response.meta['post_item']

        detail_text = sel.xpath('//*[@id="articleContent"]').xpath('string(.)').extract_first()
        post_item['content'] = detail_text

        picture_href = sel.xpath('//*[@id="articleContent"]//img/@src').extract()
        post_item['picture_hrefs'] = picture_href

        yield post_item

