#!/usr/bin python3
# -*- coding:utf-8 -*-
from scrapy import Selector

from doubanGroup.items import AuthorItem
from doubanGroup.spiders.post import get_author_id_by_head_src

check_value = lambda x: x if x else ''


def get_author_item(response):
    url = response.url
    sel = Selector(response)

    author_item = AuthorItem()
    author_item['url'] = url

    author_src = sel.xpath('//div[@class="pic"]/a/img/@src').extract_first()
    author_id = get_author_id_by_head_src(author_src)

    if not author_id:
        logoff_info = sel.xpath('//div[@class="mn"]').xpath('string(.)').extract_first()
        logoff_s = logoff_info.split('注销时间：')
        if logoff_s and len(logoff_s) > 1:
            author_item['logoff_time'] = logoff_s[-1]
        else:
            author_item['logoff_time'] = '-1'
    else:
        author_item['logoff_time'] = ''
        author_item['author_id'] = check_value(author_id)

        author_name = sel.xpath('//div[@class="info"]/h1/text()').extract_first()
        author_item['author_name'] = check_value(author_name).strip()

        signature = sel.xpath('//div[@id="display"]/text()').extract_first()
        author_item['signature'] = check_value(signature)

        location = sel.xpath('//div[@class="user-info"]/a/text()').extract_first()
        author_item['location'] = check_value(location)

        join_time = sel.xpath('//div[@class="user-info"]/div[@class="pl"]/text()').extract()[-1]
        if join_time and len(join_time) > 3:
            author_item['join_time'] = check_value(join_time).strip()[:-2]
        else:
            author_item['join_time'] = ''

        introduction = sel.xpath('//span[@id="intro_display"]').xpath('string(.)').extract_first()
        author_item['introduction'] = check_value(introduction)

    return author_item
