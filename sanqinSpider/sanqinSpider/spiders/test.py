#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider, Spider
from scrapy.spiders import Rule

from sanqinSpider.spiders.get_info import *


class Test(Spider):
    name = 'test'

    allowed_domains = ['sanqin.com']

    # start_urls = ['http://www.sanqin.com/']
    start_urls = ['http://www.sanqin.com/2015/0819/138609.shtml']

    def parse(self, response):
        item = get_dark_pic_item(response)

        return item