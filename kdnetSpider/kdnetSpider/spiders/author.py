#! /usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from kdnetSpider.items import AuthorItem, FansItem

check_value = lambda x: x if x else ''


def get_author_info(response, author_id, author_name):
    sel = Selector(response)

    author_item = AuthorItem()

    url = response.url
    author_item['url'] = url

    author_item['author_id'] = author_id
    author_item['nick'] = author_name

    tips = sel.xpath('//div[@class="useridinfo"]/div[contains(@class, "userid")]/a/@onmouseover').extract_first()

    author_item['level'] = '-1'
    author_item['influence'] = '-1'
    author_item['hits'] = '-1'
    author_item['post_num'] = '-1'
    author_item['fans_num'] = '-1'
    author_item['friends_num'] = '-1'

    if tips:
        tips_div = tips[5:-2]
        tip_sel = Selector(text=tips_div)
        info_list = tip_sel.xpath('//div[@class="cont-r"]/span/text()').extract()
        if info_list and len(info_list) > 3:
            author_item['level'] = info_list[0]
            author_item['influence'] = info_list[1]
            author_item['hits'] = info_list[2]
            author_item['fans_num'] = info_list[3]

    fans_div = sel.xpath('//ul[contains(@class, "useratten")]/li/a/strong/text()').extract()
    if fans_div:
        author_item['post_num'] = check_value(fans_div[0])
        author_item['fans_num'] = check_value(fans_div[1])
        author_item['friends_num'] = check_value(fans_div[2])

    register_div = sel.xpath('//div[contains(@class, "detailed")]/div[@class="detailed-info"]/text()').extract()
    if register_div and len(register_div) > 1:
        register_time = register_div[0].split('：')[-1].strip()
        login_num = register_div[1].split('：')[-1].strip()
    else:
        register_time = '-1'
        login_num = '-1'

    author_item['register_time'] = register_time
    author_item['login_num'] = login_num

    author_item['parse_time'] = time.time()

    return author_item


def get_author_id_by_href(author_href):
    """
    提取用户主页链接中的用户ID
    :param author_href:
    :return:
    """
    author_id = author_href.split('?')[-1].split('=')[-1]

    return author_id


def get_author_fans(response, author_id):
    for fans_item in get_fans_friends_info(response):
        fans_item['friends'] = author_id
        fans_item['fans'] = fans_item['_user_id']

        yield fans_item


def get_author_friends(response, author_id):
    for fans_item in get_fans_friends_info(response):
        fans_item['fans'] = author_id
        fans_item['friends'] = fans_item['_user_id']

        yield fans_item


def get_fans_friends_info(response):
    """
    粉丝或关注的ajax页面的用户列表
    :param response:
    :return:
    """

    sel = Selector(response)

    user_list = sel.xpath('//*[@id="SeeFollow"]/ul/div')
    for user_info in user_list:
        fans_item = FansItem()

        user_nick = user_info.xpath('./div[@class="userPic"]/a/@title').extract_first()
        user_href = user_info.xpath('./div[@class="userPic"]/a/@href').extract_first()
        if not user_href:
            continue

        user_id = get_author_id_by_href(user_href)

        fans_item['_user_id'] = check_value(user_id)
        fans_item['_user_nick'] = check_value(user_nick)
        fans_item['_user_href'] = response.urljoin(check_value(user_href))

        yield fans_item






