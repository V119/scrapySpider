#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from tianyaBBSSpider.items import AuthorItem

check_value = lambda x: x if x else ''


def get_author_item(response):
    url = response.url
    sel = Selector(response)

    author_item = AuthorItem()
    author_item['url'] = url

    author_id = sel.xpath('//a[@class="black-btn addtoblack"]/@_data').extract_first()
    author_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//div[@class="portrait"]/h2/a/text()').extract_first()
    author_item['author_name'] = check_value(author_name)

    level = sel.xpath('//div[@class="ds"]/a/text()').extract_first()
    author_item['level'] = check_value(level)

    num_div = sel.xpath('//div[@class="relate-link"]/div[@class="link-box"]')
    friends_num = num_div[0].xpath('./p/a/text()').extract_first()
    fans_num = num_div[1].xpath('./p/a/text()').extract_first()

    author_item['friends_num'] = check_value(friends_num)
    author_item['fans_num'] = check_value(fans_num)

    userinfo_div = sel.xpath('//div[@class="userinfo"]/p')
    author_item['point'] = '-1'
    author_item['login_num'] = '-1'
    author_item['register_date'] = '-1'

    for userinfo in userinfo_div:
        info_name = userinfo.xpath('./span/text()').extract_first()
        if '积　　分' in info_name:
            info_value = userinfo.xpath('./text()').extract()[-1]
            author_item['point'] = check_value(info_value)
        elif '登录次数' in info_name:
            info_value = userinfo.xpath('./text()').extract()[-1]
            author_item['login_num'] = check_value(info_value)
        elif '注册日期' in info_name:
            info_value = userinfo.xpath('./text()').extract()[-1]
            author_item['register_date'] = check_value(info_value)

    info_div = sel.xpath('//div[@class="info-wrapper"]/ul/li')
    author_item['location'] = ''
    for info in info_div:
        i_name = info.xpath('./i/@class').extract_first()
        if i_name and 'user-location' in i_name:
            i_value = info.xpath('./text()').extract()[-1]
            author_item['location'] = check_value(i_value)
        else:
            print('i class: ' + i_name + '  ' + 'i_value: ' + info.xpath('./text()').extract()[-1])

    return author_item


def get_author_id_by_href(href):
    href_s = href.split('/')
    if href_s:
        return href_s[-1]

    return None
