#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from peopleBBSSpider.items import AuthorItem
from peopleBBSSpider.utils import MD5Utils

check_value = lambda x: x if x else ''


def get_author_item(response):
    url = response.url
    sel = Selector(response)

    author_item = AuthorItem()
    author_item['url'] = url

    author_id = MD5Utils.md5_code(url)
    author_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//div[@class="people_info"]/h3/text()').extract_first()
    author_item['author_name'] = check_value(author_name).strip()

    level = sel.xpath('//div[@class="people_info"]/h3/span/text()').extract_first()
    author_item['level'] = check_value(level)

    num_div = sel.xpath('//div[@class="people_info_c"]/ul/li')

    if len(num_div) > 2:

        post_num = num_div[0].xpath('./b/text()').extract_first()
        author_item['post_num'] = check_value(post_num)

        reply_num = num_div[1].xpath('./b/text()').extract_first()
        author_item['reply_num'] = check_value(reply_num)

        elite_num = num_div[2].xpath('./b/text()').extract_first()
        author_item['elite_num'] = check_value(elite_num)

        return author_item

    return None

