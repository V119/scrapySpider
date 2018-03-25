#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from peopleSpider.spiders.get_info import *


class PeopleSpider(CrawlSpider):
    name = 'people'

    allowed_domains = ['people.com.cn']

    start_urls = ['http://www.people.com.cn/']

    article_extract = LxmlLinkExtractor(allow='/\d{4}/\d{4}/[a-zA-Z]\d+-\d+.html',
                                        allow_domains='people.com.cn',
                                        deny_domains=('tv.people.com.cn',
                                                      'bbs1.people.com.cn',
                                                      '71bbs.people.com.cn',
                                                      'chinapic.people.com.cn',
                                                      'ezheng.people.com.cn',
                                                      'ids.people.com.cn',
                                                      'comments.people.com.cn'))

    follow_extract = LxmlLinkExtractor(allow_domains='people.com.cn',
                                       deny_domains=('bbs1.people.com.cn',
                                                     '71bbs.people.com.cn',
                                                     'chinapic.people.com.cn',
                                                     'ezheng.people.com.cn',
                                                     'ids.people.com.cn',
                                                     'comments.people.com.cn'))

    rules = (Rule(article_extract, follow=True, callback='parse_article'),
             Rule(follow_extract, follow=True))

    def parse_article(self, response):
        sel = Selector(response)
        news_type_1 = sel.xpath('//div[@class="fl text_con_left"]')
        news_type_2 = sel.xpath('//div[@class="text_c"] | //div[@id="main"]/div[@id="left"]')
        pic_news = sel.xpath('//div[@id="picG"] | //div[@class="pic_content clearfix"] '
                             '| //div[@class="text width978 clearfix"]')
        section_news = sel.xpath('//section[@class="left"]')
        news_dang = sel.xpath('//font[@id="zoom"]')
        fanfu_div = sel.xpath('//div[@class="text_con text_con01"]')
        dangshi_div = sel.xpath('//div[@class="clear clearfix content_text"]')
        dangshi_2_div = sel.xpath('//div[@class="t2_left fl"]')
        qunzhong_div = sel.xpath('//div[@class="d2_left d2txt_left fl"]')
        if news_type_1:
            page_list, item = get_news_1_info(response)

            if not page_list:
                yield item
            else:
                yield Request(
                    url=page_list[1],
                    callback=self.parse_next_page,
                    meta={
                        'item': item,
                        'page_list': page_list,
                        'page_num': 2
                    }
                )
        elif news_type_2 or section_news:
            item = get_news_2_info(response)
            yield item
        elif pic_news:
            page_urls, item = get_pic_news_info(response)

            if page_urls:
                yield Request(
                    url=page_urls[0],
                    callback=self.parse_pic_next_page,
                    meta={
                        'page_urls': page_urls,
                        'page_index': 1,
                        'item': item
                    }
                )
            else:
                yield item
        elif news_dang:
            next_pages, item = get_dang_news_info(response)
            if next_pages:
                next_index = 1
                if len(next_pages) > 1:
                    yield Request(
                        url=next_pages[next_index],
                        callback=self.parse_dang_next_page,
                        meta={
                            'next_index': next_index + 1,
                            'page_urls': next_pages,
                            'item': item
                        }
                    )
                else:
                    yield item
            else:
                yield item
        elif fanfu_div:
            item = get_fanfu_info(response)

            yield item

        elif dangshi_div:
            item = get_dangshi_info(response)

            yield item

        elif dangshi_2_div:
            item = get_dangshi_2_info(response)

            yield item

        elif qunzhong_div:
            next_pages, item = get_qunzhong_info(response)
            if next_pages:
                next_index = 1
                yield Request(
                    url=response.urljoin(next_pages[next_index]),
                    callback=self.parse_qunzhong_next_page,
                    meta={
                        'item': item,
                        'page_urls': next_pages,
                        'page_index': next_index + 1
                    }
                )
            else:
                yield item

        else:
            raise ValueError('Page style not in list: ' + response.url)

    def parse_dang_next_page(self, response):
        next_index = response.meta['next_index']
        page_urls = response.meta['page_urls']
        item = response.meta['item']

        content_text, content_img_urls, content_urls = get_dang_content_div(response)

        item['content'] += content_text
        item['pictures_url'] += content_img_urls
        item['content_url'].update(content_urls)

        if len(page_urls) > next_index:
            yield Request(
                url=page_urls[next_index],
                callback=self.parse_dang_next_page,
                meta={
                    'next_index': next_index + 1,
                    'page_urls': page_urls,
                    'item': item
                }
            )
        else:
            yield item

    def parse_next_page(self, response):
        item = response.meta['item']
        page_list = response.meta['page_list']
        page_num = response.meta['page_num']

        sel = Selector(response)

        content_div = sel.xpath('//div[@id="rwb_zw"]/p')
        content = []
        img_urls = []
        for content_p in content_div:
            content_text = content_p.xpath('string(.)').extract_first()
            content.append(content_text)

            img_url = content_p.xpath('//img/@src').extract()
            if img_url:
                img_urls = img_urls + img_url

        if img_urls:
            img_urls = [response.urljoin(url) for url in img_urls if url]

        item['content'] += ''.join(content)
        item['pictures_url'] += img_urls

        if page_num < len(page_list):
            yield Request(
                url=page_list[page_num - 1],
                callback=self.parse_next_page,
                meta={
                    'item': item,
                    'page_list': page_list,
                    'page_num': page_num + 1
                }
            )

        else:
            yield item

    def parse_pic_next_page(self, response):
        page_urls = response.meta['page_urls']
        page_index = response.meta['page_index']
        item = response.meta['item']

        page_content = get_pic_content(response)
        page_pic_urls = get_pic_picture_url(response)
        item['content'].append(page_content)
        item['pictures_url'].append(page_pic_urls)

        if page_index < len(page_urls):
            yield Request(
                url=page_urls[page_index],
                callback=self.parse_pic_next_page,
                meta={
                    'page_urls': page_urls,
                    'page_index': page_index + 1,
                    'item': item
                }
            )
        else:
            yield item

    def parse_qunzhong_next_page(self, response):
        page_urls = response.meta['page_urls']
        page_index = response.meta['page_index']
        item = response.meta['item']

        page_content = get_qunzhong_content(response)
        page_pic_urls = get_qunzhong_picture(response)
        item['content'] += page_content
        item['pictures_url'].append(page_pic_urls)

        if page_index < len(page_urls):
            yield Request(
                url=response.urljoin(page_urls[page_index]),
                callback=self.parse_qunzhong_next_page,
                meta={
                    'page_urls': page_urls,
                    'page_index': page_index + 1,
                    'item': item
                }
            )
        else:
            yield item
