#!/usr/bin python3
# -*- coding: utf-8 -*-
import json

from scrapy import Selector
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from sina_news_spider.spiders.get_info import get_news_1_info, get_news_2_info, get_pic_info, get_discuss_info, \
    get_old_news_info, get_old_div_2_info


class SinaSpider(CrawlSpider):
    with open("config") as f:
        config_json = f.read()
        config_obj = json.loads(config_json)\

    name = config_obj['name']

    def __init__(self, *args, **kwargs):
        super(SinaSpider, self).__init__(*args, **kwargs)
        self.custom_settings = kwargs

    allowed_domains = ['news.sina.com.cn']

    start_urls = ['http://news.sina.com.cn/']

    article_extract = LxmlLinkExtractor(
        allow=(
            '/\d{4}-\d{2}-\d{2}/doc-[a-zA-Z]+\d+.shtml',
            '/\d{4}-\d{2}-\d{2}/\d+.shtml',
            '/slide_\d+_\d+_\d+.html'
        ),
        allow_domains=(
            'news.sina.com.cn'
        ),
        deny_domains=(
            'bbs.sina.com.cn',
            'club.mil.news.sina.com.cn'
        )
    )

    follow_extract = LxmlLinkExtractor(
        allow_domains=(
            'news.sina.com.cn'
        ),
        deny_domains=(
            'bbs.sina.com.cn',
            'club.mil.news.sina.com.cn'
        )
    )

    rules = (
        Rule(article_extract, follow=True, callback='parse_article'),
        Rule(follow_extract, follow=True, callback='parse_follow')
    )

    # a_count = 0
    # f_count = 0

    def parse_article(self, response):
        # self.a_count += 1
        # print('article:  ' + str(self.a_count) + '   ' + response.url)
        sel = Selector(response)
        news_1_div = sel.xpath('//div[@id="articleContent"]/div[@class="left"]/div[@id="artibody"]')
        news_2_div = sel.xpath('//div[@id="wrapOuter"]/div[@class="content_wrappr_left"]/div[@id="artibody"]')
        pic_div = sel.xpath('//div[@id="SI_Player"]/div[@class="part-a"] '
                            '| //div[@id="SI_Wrap"]/div[@id="SI_Slide_Wrap"]')
        discuss_div = sel.xpath('//div[@id="J_Article_Wrap"]/div[@class="blkContainerSblk"]')
        old_news_div = sel.xpath('//div[@class="blkContainer"]//div[@class="blkContainerSblk"]')
        old_news_2_div = sel.xpath('//td[@class="lc_blue"]/div[@class="lcBlk"]')
        old_news_3_div = sel.xpath('//*[@id="outer"]/table')

        if news_1_div:
            news_item = get_news_1_info(response)
        elif news_2_div:
            news_item = get_news_2_info(response)
        elif pic_div:
            news_item = get_pic_info(response)
        elif discuss_div:
            news_item = get_discuss_info(response)
        elif old_news_div:
            news_item = get_old_news_info(response)
        elif old_news_2_div:
            news_item = get_old_div_2_info(response)
        elif old_news_3_div:
            pass

        else:
            raise AttributeError(response.url)

        return news_item

    def parse_follow(self, response):
        # self.f_count += 1
        # print('follow:  ' + str(self.f_count) + '   ' + response.url)
        pass

