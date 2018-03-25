#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from wangyiNewsSpider.items import NewsItem


def get_news_1_info(response):
    news_item = NewsItem()

    news_item['url'] = response.url
    news_item['spider_time'] = time.time()

    sel = Selector(response)

    keywords = sel.xpath('//')
