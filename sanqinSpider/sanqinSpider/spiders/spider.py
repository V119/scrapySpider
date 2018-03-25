#!/usr/bin python3
# -*- coding: utf-8 -*-
import json

from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from sanqinSpider.spiders.get_info import *
from sanqinSpider.utils.page_utils import get_all_content_url


class SanqinSpider(CrawlSpider):
    name = 'sanqin'

    allowed_domains = ['sanqin.com']

    # start_urls = ['http://www.sanqin.com/']
    start_urls = ['http://www.sanqin.com/news/live/']

    article_extract = LxmlLinkExtractor(allow='/\d{4}/\d{4}/\d+.shtml',
                                        allow_domains='sanqin.com',
                                        deny_domains=('epaper.sanqin.com',
                                                      'bbs.sanqin.com',
                                                      'car.sanqin.com/'))

    follow_extract = LxmlLinkExtractor(allow_domains='sanqin.com',
                                       deny_domains=('epaper.sanqin.com',
                                                     'bbs.sanqin.com',
                                                     'car.sanqin.com/'))

    rules = (Rule(article_extract, follow=True, callback='parse_article'),
             Rule(follow_extract, follow=True, callback='parse_page_link'))

    # a_count = 0
    # f_count = 0

    def parse_article(self, response):
        # self.a_count += 1
        # print(str(self.a_count) + '  article:    ' + response.url)
        sel = Selector(response)
        news_div = sel.xpath('//div[@id="container"]/div[@class="node-box"]')
        pic_div = sel.xpath('//div[@class="column article-content pos-r js-returntop"]'
                            '/div[@class="gallery_wrap pos-r"]')
        dark_pic_div = sel.xpath('//div[@id="gallery"]')
        if news_div:
            content_id, item = get_news_info(response)
            if content_id:
                # 全部文章的URL
                all_content_url = get_all_content_url(content_id)
                yield Request(
                    url=all_content_url,
                    callback=self.join_all_content,
                    meta={
                        'item': item
                    }
                )
        elif pic_div:
            item = get_pic_item(response)

            yield item
        elif dark_pic_div:
            item = get_dark_pic_item(response)

            yield item
        else:
            raise ValueError(response.url)

    def parse_page_link(self, response):
        url = response.url
        # self.f_count += 1
        # print(str(self.f_count) + '  follow:    ' + url)

        # 如果是第二十页，试图去访问没有直接链接的第21页
        if url.endswith('/20.shtml'):
            yield Request(response.urljoin('21.shtml'))

    def join_all_content(self, response):
        item = response.meta['item']
        img_urls, content_text = get_all_content(response)
        if img_urls:
            item['picture_urls'] = img_urls

        if content_text:
            item['content'] = content_text

        yield item
