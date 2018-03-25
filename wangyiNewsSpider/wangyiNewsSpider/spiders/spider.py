#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule


class WangyiNewsSpider(CrawlSpider):
    name = '163_news'

    allowed_domains = ['news.163.com']

    start_urls = ['http://news.163.com/']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/\d{2}/\d{4}/\d{2}/[a-zA-Z0-9_]+.html',
            'photoview/[a-zA-Z0-9]+/\d+.html',
            '/\d+/\d+/[A-Z0-9]+.html',
            '/photo/[A-Z0-9]+/\d+.html',
            '/\d+/\d/[a-zA-Z0-9_]+.html'
        ),
        allow_domains=(
            'news.163.com'
        )
    )

    follow_extract = LxmlLinkExtractor(
        allow_domains=(
            'news.163.com'
        )
    )

    rules = (
        Rule(article_extract, follow=True, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )

    a_count = 0
    f_count = 0

    def parse_article(self, response):
        self.a_count += 1
        print('article:  ' + str(self.a_count) + '   ' + response.url)

        sel = Selector(response)
        # http://news.163.com/17/0117/14/CB07N4J4000187VE.html
        news_1_div = sel.xpath('//div[@id="epContentLeft"]/div[@id="post_body"]')

    def parse_follow(self, response):
        self.f_count += 1
        print('follow:  ' + str(self.f_count) + '   ' + response.url)
