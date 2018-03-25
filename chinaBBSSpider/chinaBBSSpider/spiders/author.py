#!/usr/bin python3
# -*- coding:utf-8 -*-
import time
from scrapy import Selector

from chinaBBSSpider.items import AuthorItem

check_value = lambda x: x if x else ''


def get_author_item(response):
    url = response.url
    sel = Selector(response)

    author_item = AuthorItem()
    author_item['url'] = url

    author_id = sel.xpath('//input[@id="_userid"]/@value').extract_first()
    author_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//*[@id="tagid"]').xpath('string(.)').extract_first()
    author_item['author_name'] = check_value(author_name)

    focuse_num = sel.xpath('//span[@class="guanzhuWidthLeft"]/a/text()').extract_first()
    author_item['focuse_num'] = check_value(focuse_num)

    fans_num = sel.xpath('//span[@class="guanzhuWidthRight"]/a/text()').extract_first()
    author_item['fans_num'] = check_value(fans_num)

    info_div = sel.xpath('//div[@class="mod cardStatus"]/dl[@class="medal"]')

    author_item['name'] = ''
    author_item['sex'] = ''
    author_item['birthday'] = ''
    author_item['address'] = ''

    for info_sel in info_div:
        info_text = info_sel.xpath('./dt/text()').extract_first()
        info_value = info_sel.xpath('./dd').extract_first()
        if '姓名' in info_text:
            author_item['name'] = check_value(info_value)
        elif '性别' in info_text:
            author_item['sex'] = check_value(info_value)
        elif '生日' in info_text:
            author_item['birthday'] = check_value(info_value)
        elif '地址' in info_text:
            author_item['address'] = check_value(info_value)

    parse_time = time.time()
    author_item['parse_time'] = parse_time

    return author_item



