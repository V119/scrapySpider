#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Spider
from scrapy.spiders import Rule

from sina_news_spider.spiders.get_info import get_pic_info, get_old_3_info


class Test(Spider):
    name = 'test'

    allowed_domains = ['news.sina.com.cn']

    # start_urls = ['http://www.sanqin.com/']
    start_urls = ['http://news.sina.com.cn/w/2006-08-21/100410783609.shtml']

    def parse(self, response):
        sel = Selector(response)
        pic_div = sel.xpath('//div[@id="SI_Player"]/div[@class="part-a"] '
                            '| //div[@id="SI_Wrap"]/div[@id="SI_Slide_Wrap"]')
        item = get_old_3_info(response)

        return item
