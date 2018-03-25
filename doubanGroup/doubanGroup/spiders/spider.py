#!/usr/bin python3
# -*- coding:utf8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from doubanGroup.items import FansItem
from doubanGroup.spiders.author import get_author_item
from doubanGroup.spiders.comment import get_comment_list, get_next_page_href
from doubanGroup.spiders.fans import get_fans_page_url, get_fans_ids, get_fans_next_page_url, get_friends_page_url
from doubanGroup.spiders.group import get_group_item
from doubanGroup.spiders.post import get_post_item
from doubanGroup.utils.login_api import get_login_cookie


class DoubanGroupSpider(CrawlSpider):
    name = 'douban_group'

    start_urls = [
        'https://www.douban.com/group/',
        # 'https://www.douban.com/group/topic/98147436/',
    ]

    allowed_domains = [
        'www.douban.com'
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        # if os.path.exists(settings.COOKIE_FILE):
        #     os.remove(settings.COOKIE_FILE)

        self.cookies = get_login_cookie(self.start_urls[0])

    post_extract = LxmlLinkExtractor(
        allow=(
            '/group/topic/\d+/$',
            '/group/topic/\d+$',
        ),
        allow_domains=(
            'douban.com'
        ),
        deny=(
            '/accounts/login',
            '/login\?redir',
        ),
        # deny_domains=(
        #
        # )
    )

    author_extract = LxmlLinkExtractor(
        allow=(
            '/people/\w+/$',
            '/people/\w+$',
        ),
        allow_domains=(
            'douban.com',
        ),
        deny=(
            '/accounts/login',
            '/login\?redir',
        ),
        # deny_domains=(
        #
        # )
    )

    group_extract = LxmlLinkExtractor(
        allow=(
            '/group/\w+/$',
            '/group/\w+$',
        ),
        allow_domains=(
            'douban.com',

        ),
        deny=(
            '/group/explore',
            '/accounts/login',
            '/login\?redir',
        ),
    )

    follow_extract = LxmlLinkExtractor(
        allow=(
            '/people/',
            '/group/',
        ),
        allow_domains=(
            'douban.com',
        ),
        deny=(
            '\?action=join',
            '/feed/group/',
            '/rev_contacts\?start=',
            '/accounts/login',
        ),
        # deny_domains=(
        #     'q.blog.sina.com.cn'
        # )
    )

    rules = (
        Rule(author_extract, follow=False, callback='parse_author', process_request='add_cookies'),
        Rule(group_extract, follow=True, callback='parse_group', process_request='add_cookies'),
        Rule(post_extract, follow=True, callback='parse_post', process_request='add_cookies'),
        Rule(follow_extract, follow=True, callback='parse_follow', process_request='add_cookies'),
        # Rule(follow_extract, follow=True, process_request='add_cookies'),
    )

    def add_cookies(self, request):
        request.replace(cookies=self.cookies)

        return request
    #
    a_count = 0
    p_count = 0
    f_count = 0
    g_count = 0
    fa_count = 0

    def parse_author(self, response):
        # self.a_count += 1
        # print('author: ', self.a_count, '  ', response.url)
        author_item = get_author_item(response)

        # 获取粉丝和关注列表
        fans_url = get_fans_page_url(response)
        yield Request(
            url=fans_url,
            callback=self.parse_fans,
            meta={
                'user_id': author_item['author_id'],
            }
        )

        friends_url = get_friends_page_url(response)
        yield Request(
            url=friends_url,
            callback=self.parse_friends,
            meta={
                'user_id': author_item['author_id'],
            }
        )

        yield author_item

    def parse_group(self, response):
        # self.g_count += 1
        # print('group: ', self.g_count, '  ', response.url)
        group_item = get_group_item(response)

        yield group_item

    def parse_post(self, response):
        # self.p_count += 1
        # print('post: ', self.p_count, '  ', response.url)
        post_item = get_post_item(response)

        for item_or_request in self.parse_comment(response, post_item):
            yield item_or_request

    def parse_follow(self, response):
        self.f_count += 1
        print('follow: ', self.f_count, '  ', response.url)

    def parse_comment(self, response, post_item=None):
        if not post_item:
            post_item = response.meta['post_item']

        post_id = post_item['post_id']

        for comment_item in get_comment_list(response, post_id):
            comment_id = comment_item['comment_id']
            post_item['comment_ids'].append(comment_id)

            yield comment_item

        next_page = get_next_page_href(response)

        if next_page:
            yield Request(
                url=next_page,
                callback=self.parse_comment,
                meta={
                    'post_item': post_item
                }
            )

        else:
            yield post_item

    def parse_fans(self, response):
        user_id = response.meta['user_id']

        for fans_id in get_fans_ids(response):
            fans_item = FansItem()

            fans_item['fans_id'] = fans_id
            fans_item['friends_id'] = user_id

            yield fans_item

        next_page = get_fans_next_page_url(response)

        if next_page:
            yield Request(
                url=next_page,
                callback=self.parse_fans,
                meta={
                    'user_id': user_id,
                }
            )

    def parse_friends(self, response):
        user_id = response.meta['user_id']

        for fans_id in get_fans_ids(response):
            fans_item = FansItem()

            fans_item['fans_id'] = fans_id
            fans_item['friends_id'] = user_id

            yield fans_item
