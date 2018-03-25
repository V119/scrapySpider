#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Spider
from scrapy.spiders import Rule

from peopleSpider.spiders.get_info import *


class Test(Spider):
    name = 'test'

    allowed_domains = ['people.com.cn']

    # start_urls = ['http://www.sanqin.com/']
    start_urls = ['http://qzlx.people.com.cn/n/2014/0515/c364565-25020276.html']

    def parse(self, response):
        sel = Selector(response)
        news_type_1 = sel.xpath('//div[@class="fl text_con_left"]')
        news_type_2 = sel.xpath('//div[@class="text_c"] | //div[@id="main"]/div[@id="left"]')
        pic_news = sel.xpath('//div[@id="picG"] | //div[@class="pic_content clearfix"] '
                             '| //div[@class="text width978 clearfix"]')
        dang_news = sel.xpath('//font[@id="zoom"]')
        fanfu_div = sel.xpath('//div[@class="text_con text_con01"]')
        dangshi_div = sel.xpath('//div[@class="clear clearfix content_text"] | div[@class="t2_left fl"]')
        dangshi_2_div = sel.xpath('//div[@class="t2_left fl"]')
        qunzhong_div = sel.xpath('//div[@class="d2_left d2txt_left fl"]')
        item = get_qunzhong_info(response)

        return item
