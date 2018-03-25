#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from newsBBSSpider.items import AuthorItem

check_value = lambda x: x if x else ''


def get_author_item(response):
    url = response.url
    sel = Selector(response)

    author_item = AuthorItem()
    author_item['url'] = url

    author_id = gen_author_id(url)
    author_item['author_id'] = author_id

    author_name = sel.xpath('//ul[contains(@class, "lt-ind-zl")]/li[2]/text()').extract_first()
    author_item['author_name'] = author_name.split('： ')[-1]

    post_num = sel.xpath('//ul[contains(@class, "lt-ind2")]/li[1]/span[@class="t1"]/text()').extract_first()
    author_item['post_num'] = check_value(post_num)

    level = sel.xpath('//ul[contains(@class, "lt-ind2")]/li[3]/span[@class="t1"]/text()').extract_first()
    author_item['level'] = check_value(level)

    login_num = sel.xpath('//ul[contains(@class, "lt-ind-zl")]/li[3]/text()').extract_first()
    author_item['login_num'] = login_num.split('： ')[-1]

    register_time = sel.xpath('//ul[contains(@class, "lt-ind-zl")]/li[4]/text()').extract_first()
    author_item['register_time'] = register_time.split('： ')[-1]

    parse_time = time.time()
    author_item['parse_time'] = parse_time

    return author_item


def gen_author_id(author_href):
    if not author_href:
        return '_'

    elif '/portal/' in author_href:
        author_id = author_href.split('/')
        if author_id and len(author_id) > 3:
            return author_id[2].split('.')[0]

    return author_href.split('?id=')[-1]



