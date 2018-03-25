#!/usr/bin python3
# -*- coding:utf-8 -*-
from scrapy import Selector

from blog163Spider.items import AuthorItem
from blog163Spider.utils import MD5Utils

check_value = lambda x: x if x else ''


def get_author_item(response):
    sel = Selector(response)
    url = response.url

    author_item = AuthorItem()
    author_item['url'] = check_value(url)

    author_id = get_author_by_href(url)
    author_item['id'] = check_value(author_id)

    basic_info = sel.xpath('//table[@class="dtab"]')[0]
    info_list = basic_info.xpath('./tr')
    for info in info_list:
        info_name = info.xpath('./td[contains(@class, "lst")]/text()').extract_first()
        info_value = info.xpath('./td[@class="cnt"]/text()').extract_first()
        if '昵    称' in info_name:
            author_item['nick'] = check_value(info_value)
        elif '真实姓名' in info_name:
            author_item['real_name'] = check_value(info_value)
        elif '性    别' in info_name:
            author_item['sex'] = check_value(info_value)
        elif '生    日' in info_name:
            author_item['birthday'] = check_value(info_value)
        elif '故    乡' in info_name:
            author_item['hometown'] = check_value(info_value)
        elif '现居住地' in info_name:
            author_item['apartment'] = check_value(info_value)
        elif '自我介绍' in info_name:
            author_item['introduce'] = check_value(info_value)
        elif '近期心愿' in info_name:
            author_item['wish'] = check_value(info_value)
        elif '加入的圈子' in info_name:
            author_item['circle'] = check_value(info_value)
        else:
            print('error value!! ' + info_name)

    information = sel.xpath('//table[@class="dtab"]')[1].xpath('string(.)').extract_first()
    author_item['information'] = check_value(information)

    experience = sel.xpath('//div[@class="biograph"]').xpath('string(.)').extract_first()
    author_item['experience'] = check_value(experience)

    contact = sel.xpath('//table[@class="fs0"]').xpath('string(.)').extract_first()
    author_item['contact'] = check_value(contact)

    return author_item


def get_author_by_href(author_href):
    result = MD5Utils.md5_code(author_href.split('/')[0])
    return result
