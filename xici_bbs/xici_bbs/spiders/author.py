#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from xici_bbs.items import AuthorItem

check_value = lambda x: x if x else ''


def get_author_item(response):
    sel = Selector(response)
    url = response.url

    author_item = AuthorItem()
    author_item['author_href'] = url

    author_item['parse_time'] = time.time()

    author_name = sel.xpath('//div[@class="cul"]/p[@class="name"]').xpath('string(.)').extract_first()
    author_item['author_name'] = check_value(author_name)

    info_div = sel.xpath('//div[@class="cul"]/ul/li')
    id_div = info_div[0].xpath('./text()').extract_first()
    if id_div:
        author_item['author_id'] = check_value(id_div.split('：')[-1])
    else:
        author_item['author_id'] = ''

    register_div = info_div[1].xpath('./text()').extract_first()
    if register_div:
        author_item['register_time'] = check_value(register_div.split('：')[1])
    else:
        author_item['register_time'] = ''

    return
