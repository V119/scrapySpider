#!/usr/bin python3
# -*- coding: utf-8 -*-
import json

from scrapy import Selector


def get_fans_next_page(response, page_num, type_p):
    href = '/portal/attentionList/' + str(page_num) + '/10?type=' + str(type_p) + '&privacy=false'
    return response.urljoin(href)


def get_total_page_num(response):
    sel = Selector(response)
    total_num = sel.xpath('//input[@class="totalpagenum"]/@value').extract_first()

    page_num = int(total_num) // 10 + 1

    return page_num


def get_fans_list(response):
    text = response.text

    # noinspection PyBroadException
    try:
        json_obj = json.loads(text)
        user_list = json_obj['content']['itemList']

        for user_item in user_list:
            user_id = user_item['loginName']

            yield user_id
    except:
        print('parse fans json error!!!!')
