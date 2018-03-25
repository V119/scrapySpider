#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from chinaBBSSpider.spiders.author import get_author_item
from chinaBBSSpider.spiders.comment import get_comment_url, get_comment_list, get_comment_prise
from chinaBBSSpider.spiders.post import get_post_item, get_post_next_page, get_content, parse_num_js


class ChinaBBSSpider(CrawlSpider):
    name = 'china_bbs'

    start_urls = ['http://club.china.com/']

    post_extract = LxmlLinkExtractor(
        allow=(
            '/data/thread/\d+/\d+/\d+/\d+/\d+_1.html',
        ),
        allow_domains=(
            'club.china.com'
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
            '/jsp/personalinfo/',
            'UserInfoAction\.do\?'
        ),
        allow_domains=(
            'club.china.com',
        ),
        deny=(

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
            'club.china.com',
        ),
        deny=(
            '/data/thread/\d+/\d+/\d+/\d+/\d+_\d+_\d+.html'
        ),
        deny_domains=(
            'tuku.club.china.com'
        )
    )

    rules = (
        Rule(author_extract, follow=True, callback='parse_author'),
        Rule(post_extract, follow=True, callback='parse_post'),
        # Rule(follow_extract, follow=True, callback='parse_follow'),
        Rule(follow_extract, follow=True),
    )
    #
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

        for post_request in self.parse_post_continue(response, post_item):
            yield post_request

    # def parse_follow(self, response):
    #     self.f_count += 1
    #     print('follow: ', self.f_count, '  ', response.url)

    def parse_post_continue(self, response, post_item=None):
        if not post_item:
            post_item = response.meta['post_item']
            content, picture_hrefs = get_content(response)
            post_item['content'] = post_item['content'] + content
            post_item['picture_hrefs'] = post_item['picture_hrefs'] + picture_hrefs

        next_page = get_post_next_page(response)

        if next_page:
            yield Request(
                url=next_page,
                callback=self.parse_post_continue,
                meta={
                    'post_item': post_item,
                }
            )
        else:
            for comment_item_request in self.parse_comment(response, post_item):
                yield comment_item_request

    def parse_num_div(self, response):
        post_item = response.meta['post_item']

        read_num, part_num, reply_num = parse_num_js(response)

        post_item['read_num'] = read_num
        post_item['participant_num'] = part_num
        post_item['reply_num'] = reply_num

        yield post_item

    def parse_comment(self, response, post_item=None):
        has_next_page = True

        if not post_item:
            post_item = response.meta['post_item']
            page_num = response.meta['page_num']

            post_id = post_item['post_id']

            prise_dict = response.meta['prise_dict']

            last_floor = 0
            for comment_item in get_comment_list(response, post_id):
                last_floor = comment_item['floor']
                post_item['comment_ids'].append(comment_item['comment_id'])
                comment_item['prise_num'] = prise_dict.get(str(comment_item['comment_id']), '0')

                yield comment_item

            if int(last_floor) < (page_num - 1) * 100:
                has_next_page = False

        else:
            page_num = 1
            prise_dict = get_comment_prise(response)

        if has_next_page:
            comment_url = get_comment_url(response, page_num)
            yield Request(
                url=comment_url,
                callback=self.parse_comment,
                meta={
                    'post_item': post_item,
                    'page_num': page_num + 1,
                    'prise_dict': prise_dict,
                }
            )
        else:
            num_href = post_item['_num_href']
            yield Request(
                url=num_href,
                callback=self.parse_num_div,
                meta={
                    'post_item': post_item,
                }
            )
