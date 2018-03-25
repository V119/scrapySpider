#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from tianyaBBSSpider.items import CommentItem
from tianyaBBSSpider.spiders.author import get_author_id_by_href

check_value = lambda x: x if x else ''


def get_comment_item(response):
    sel = Selector(response)

    comment_divs = sel.xpath('//div[@class="articlecomments-cell"]')
    for comment_sel in comment_divs:
        comment_item = CommentItem()

        author_name = comment_sel.xpath('./div[contains(@class, "comments-infor")]'
                                        '/a[contains(@class, "replyName")]/text()').extract_first()
        comment_item['author_name'] = check_value(author_name)

        author_href = comment_sel.xpath('./div[contains(@class, "comments-infor")]'
                                        '/a[contains(@class, "replyName")]/@href').extract_first()
        comment_item['author_href'] = check_value(author_href)

        author_id = get_author_id_by_href(author_href)
        comment_item['author_id'] = check_value(author_id)

        comment_id = comment_sel.xpath('./div[contains(@class, "comments-infor")]'
                                       '/div[@class="fr"]/a[@class="delComment"]/@data').extract_first()
        comment_item['comment_id'] = check_value(comment_id)

        content = comment_sel.xpath('./div[@class="comments-content"]').xpath('string(.)').extract_first()
        comment_item['content'] = check_value(content)

        date_time = comment_sel.xpath('./div[contains(@class, "comments-infor")]'
                                      '/div[@class="fr"]/span[contains(@class, "replyTime")]/text()').extract_first()
        comment_item['date_time'] = check_value(date_time)

        yield comment_item

def get_comment_next_page(response):
    sel = Selector(response)
    next_page_div = sel.xpath('//div[@class="pages pos-relative"]/a')
    if next_page_div:
        for href_sel in reversed(next_page_div):
            page_text = href_sel.xpath('./text()').extract_first()
            if '下一页' in page_text:
                page_href = href_sel.xpath('./@href').extract_first()

                return page_href

    return None

