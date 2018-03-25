#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from xici_bbs.items import CommentItem

check_value = lambda x: x if x else ''


def get_comment_list(response):
    sel = Selector(response)
    post_id = sel.xpath('//input[@name="lDocId"]/@value').extract_first()

    comment_div = sel.xpath('//div[@class="doc_sp doc_td2" and @id]')
    for comment_sel in comment_div[1:]:
        comment_item = CommentItem()
        comment_item['post_id'] = check_value(post_id)

        comment_item['parse_time'] = time.time()

        floor_id = comment_sel.xpath('./@id').extract_first()
        floor = floor_id[5:]

        comment_item['floor'] = check_value(floor)
        comment_item['comment_id'] = post_id + '_' + floor

        author_id = comment_sel.xpath('./div[@class="td_l"]/div/a/span/text()').extract_first()
        comment_item['author_id'] = check_value(author_id)

        author_name = comment_sel.xpath('./div[@class="td_l"]/div/a/@title').extract_first()
        comment_item['author_name'] = check_value(author_name)

        author_href = comment_sel.xpath('./div[@class="td_l"]/div/a/@href').extract_first()
        if author_href:
            comment_item['author_href'] = response.urljoin(author_href)
        else:
            comment_item['author_href'] = ''

        date_time = comment_sel.xpath('./div[@id="td_r"]/div/div[@class="l"]/b/text()').extract_first()
        comment_item['date_time'] = check_value(date_time)

        content = comment_sel.xpath('./div[@id="td_r"]/div/div[@class="doc_txt"]').xpath('string(.)').extract_first()
        comment_item['content'] = check_value(content)

        picture_href = comment_sel.xpath('./div[@id="td_r"]/div/div[@class="doc_txt"]'
                                         '//img[not(@data-baiduimageplus-ignore)]/@src').extract()
        comment_item['picture_hrefs'] = picture_href

        yield comment_item


def get_comment_next_page(response):
    sel = Selector(response)
    page_div = sel.xpath('//*[@id="page"]/a')
    for page_sel in page_div:
        page_text = page_sel.xpath('./@title').extract_first()
        if '下一页' in page_text:
            page_href = page_sel.xpath('./@href').extract_first()
            if page_href:
                return response.urljoin(page_href)

    return None

