#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from mopSpider.items import AuthorItem

check_value = lambda x: x if x else ''


def get_author_item(response):
    url = response.url

    sel = Selector(response)

    author_item = AuthorItem()
    author_item['url'] = url

    author_id = sel.xpath('//input[@class="right-page-uid"]/@value').extract_first()
    author_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//a[@class="hpUserName"]').xpath('string(.)').extract_first()
    author_item['author_name'] = check_value(author_name)

    age = sel.xpath('//div[@class="lh25 mb15 clearBoth"]/span[last()]/text()').extract_first()
    author_item['age'] = check_value(age)

    level = sel.xpath('//div[contains(@class, "levelBox")]/div/a/span/span/text()').extract_first()
    author_item['level'] = check_value(level).strip()

    level_info_div = sel.xpath('//div[contains(@class, "hpUserInfoLevel")]/ul/li')
    for level_info in level_info_div:
        info_name = level_info.xpath('./span/text()').extract_first()
        if info_name and '称号' in info_name:
            info_value = level_info.xpath('./text()').extract()[-1]
            author_item['level_nick'] = check_value(info_value)
        elif info_name and '性别' in info_name:
            info_value = level_info.xpath('./text()').extract()[-1]
            author_item['sex'] = check_value(info_value)

    num_div = sel.xpath('//div[contains(@class, "user-sns-count")]/ul/li')
    for li_div in num_div:
        li_name = li_div.xpath('//div[contains(@class, "user-sns-count")]/ul/li/p/text()').extract_first()
        li_value = li_div.xpath('//div[contains(@class, "user-sns-count")]/ul/li/p/a/text()').extract_first()

        if '积分' in li_name:
            author_item['point'] = check_value(li_value)

    hits = sel.xpath('//span[@class="tah cb00 bold num h-pageView"]/@title').extract_first()
    author_item['hits'] = check_value(hits)

    register_date = sel.xpath('//div[@class="hpUserInfo2"]/p/span/text()').extract_first()
    author_item['register_date'] = check_value(register_date)

    league = sel.xpath('//div[@class="hpUserInfo2"]/p/a/text()').extract_first()
    if not league:
        league = '无'
    author_item['league'] = check_value(league)

    user_info_div = sel.xpath('//ul[contains(@class, "hpUserInfoUl")]/li')
    for user_info in user_info_div:
        user_info_name = user_info.xpath('./div[contains(@class, "c999")]/text()').extract_first()
        user_info_value = user_info.xpath('./div[@class="oh"]/text()').extract_first()
        if '生日' in user_info_name:
            author_item['birthday'] = check_value(user_info_value)
        elif '登录次数' in user_info_name:
            author_item['login_num'] = check_value(user_info_value)
        elif '个人介绍' in user_info_name:
            author_item['introduce'] = check_value(user_info_value)

    contact_way = sel.xpath('//div[contains(@class, "homepageContent")]/div[2]').xpath('string(.)').extract_first()
    author_item['contact_way'] = check_value(contact_way)

    education = sel.xpath('//div[contains(@class, "homepageContent")]/div[3]').xpath('string(.)').extract_first()
    author_item['education'] = check_value(education)

    career = sel.xpath('//div[contains(@class, "homepageContent")]/div[4]').xpath('string(.)').extract_first()
    author_item['career'] = check_value(career)

    return author_item
