#!/usr/bin python3
# -*- coding:utf-8 -*-
import time
from scrapy import Selector

from newsBBSSpider.items import CommentItem
from newsBBSSpider.spiders.author import gen_author_id

check_value = lambda x: x if x else ''


def get_comment_list(response):
    sel = Selector(response)
    post_id = sel.xpath('//input[@name="parentid"]/@value').extract_first()

    comment_div = sel.xpath('//div[@id="postreply"]/dl/dd')
    for comment_sel in comment_div:
        comment_item = CommentItem()
        comment_item['post_id'] = check_value(post_id)

        comment_id = comment_sel.xpath('./ul[contains(@class, "ul2")]/li/a/label/@id').extract_first()
        comment_item['comment_id'] = comment_id[3:] if comment_id and len(comment_id) > 3 else '_'

        prise_num = comment_sel.xpath('./ul[contains(@class, "ul2")]/li/a/label/text()').extract_first()
        comment_item['prise_num'] = check_value(prise_num)

        author_name = comment_sel.xpath('./ul[contains(@class, "ul1")]/li'
                                        '/a[contains(@id, "user")]/text()').extract_first()
        comment_item['author_name'] = check_value(author_name)

        author_url = comment_sel.xpath('./ul[contains(@class, "ul1")]/li'
                                       '/a[contains(@id, "user")]/@href').extract_first()
        comment_item['author_href'] = check_value(author_url)

        comment_item['author_id'] = gen_author_id(author_url)

        floor_name = comment_sel.xpath('./ul[contains(@class, "ul1")]/li'
                                       '/span[contains(@id, "count")]/text()').extract_first()
        comment_item['floor'] = floor_name[:-1] if floor_name and len(floor_name) > 1 else ''

        date_time = comment_sel.xpath('./ul[contains(@class, "ul1")]/li'
                                      '/span[contains(@id, "time")]/text()').extract_first()
        comment_item['date_time'] = date_time[:-2] if date_time and len(date_time) > 2 else ''

        content = comment_sel.xpath('./div[contains(@id, "message11")]/p').xpath('string(.)').extract()
        comment_item['content'] = ''.join(content) if content else ''

        refer = comment_sel.xpath('./div[contains(@id, "message11")]/div[@class="BBS_QUOTE"]')\
            .xpath('string(.)').extract_first()
        comment_item['refer'] = check_value(refer)

        picture_href = comment_sel.xpath('./div[contains(@id, "message11")]/img/@src').extract()
        comment_item['picture_hrefs'] = picture_href

        comment_item['parse_time'] = time.time()

        yield comment_item


def get_next_page_url(response):
    sel = Selector(response)
    page_div = sel.xpath('//div[@id="postreply"]/div[contains(@class, "lt-page")]/ul[contains(@class, "fr")]/li/a')
    for page_sel in page_div:
        page_text = page_sel.xpath('./text()').extract_first()
        if '>' in page_text:
            page_href = page_sel.xpath('./@href').extract_first()
            return response.urljoin(page_href)

    return None
