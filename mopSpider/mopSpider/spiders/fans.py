#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector


def get_fans_item(response):
    sel = Selector(response)
    fans_div = sel.xpath('//div[contains(@class, "homepageContent")]/ul/li')
    fans_url_list = []
    for fans_sel in fans_div:
        fans_id = fans_sel.xpath('./div[contains(@class, "following-userInfo")]/div[@class="clearfix"]'
                                 '/div[@class="fr"]/a/@data').extract_first()
        fans_url = fans_sel.xpath('./div[contains(@class, "following-userInfo")]/div[@class="clearfix"]'
                                 '/div[@class="fl"]/a/@href').extract_first()
        if fans_url and fans_url.strip():
            fans_url_list.append((fans_id, response.urljoin(fans_url.strip())))

    return fans_url_list

