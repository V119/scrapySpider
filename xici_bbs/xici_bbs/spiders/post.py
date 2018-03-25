#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from xici_bbs.items import PostItem

check_value = lambda x: x if x else ''


def get_post_item(response):
    sel = Selector(response)
    url = response.url

    post_item = PostItem()
    post_item['url'] = url

    post_item['parse_time'] = time.time()

    post_id = sel.xpath('//input[@name="lDocId"]/@value').extract_first()
    post_item['post_id'] = check_value(post_id)

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    post_item['key_words'] = check_value(key_words)

    title = sel.xpath('//title/text()').extract_first()
    if title:
        post_item['title'] = check_value(title.split('_')[0])
    else:
        post_item['title'] = ''

    author_id = sel.xpath('//div[@class="doc_n"]/div/div/a/span/text()').extract_first()
    post_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//div[@class="doc_n"]/div/div/a/@title').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_href = sel.xpath('//div[@class="doc_n"]/div/div/a/@href').extract_first()
    post_item['author_href'] = ''
    if author_href:
        post_item['author_href'] = response.urljoin(author_href)

    date_time = sel.xpath('//div[@class="doc_n"]//div[@class="l"]/b/text()').extract_first()
    post_item['date_time'] = check_value(date_time)

    content = sel.xpath('//div[@class="doc_n"]/div[@id="td_r"]/div/div[@class="doc_txt"]')\
        .xpath('string(.)').extract_first()
    post_item['content'] = check_value(content)

    picture_href = sel.xpath('//div[@class="doc_n"]/div[@id="td_r"]/div/div[@class="doc_txt"]'
                             '//img[not(@data-baiduimageplus-ignore)]/@src').extract()
    post_item['picture_hrefs'] = picture_href

    post_item['comment_ids'] = []

    return post_item


