#!/usr/bin python3
# -*- coding:utf-8 -*-
from scrapy import Selector

from doubanGroup.spiders.post import get_author_id_by_head_src


def get_fans_ids(response):
    sel = Selector(response)
    fans_list = sel.xpath('//div[@class="article"]/dl[@class="obu"]')

    for fans_sel in fans_list:
        fans_pic = fans_sel.xpath('./dt/a/img/@src').extract_first()

        yield get_author_id_by_head_src(fans_pic)


def get_fans_page_url(response):
    sel = Selector(response)

    fans_page_url = sel.xpath('//p[@class="rev-link"]/a/@href').extract_first()

    return fans_page_url


def get_friends_page_url(response):
    sel = Selector(response)

    friends_page_url = sel.xpath('//div[@id="friend"]/h2/span[@class="pl"]/a/@href').extract_first()

    return friends_page_url


def get_fans_next_page_url(response):
    sel = Selector(response)
    next_page_url = sel.xpath('//span[@class="next"]/a/@href').extract_first()

    return next_page_url
