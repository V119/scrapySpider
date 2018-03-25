#!/usr/bin python3
# -*- coding:utf-8 -*-
import time
from scrapy import Selector

from peopleBBSSpider.items import PostItem
from peopleBBSSpider.utils import MD5Utils

check_value = lambda x: x if x else ''


def get_post_item(response):
    url = response.url
    sel = Selector(response)
    post_item = PostItem()

    post_item['url'] = url

    post_id = sel.xpath('//meta[@name="contentid"]/@content').extract_first()
    post_item['post_id'] = check_value(post_id)

    title = sel.xpath('//div[@class="navBar"]/h2/text()').extract_first()
    post_item['title'] = check_value(title)

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    post_item['key_words'] = check_value(key_words)

    author_name = sel.xpath('//a[contains(@class, "userNick")]/font/text()').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_href = sel.xpath('//a[contains(@class, "userNick")]/@href').extract_first()
    post_item['author_href'] = check_value(author_href)

    if author_href:
        author_id = MD5Utils.md5_code(author_href)
        post_item['author_id'] = author_id
    else:
        post_item['author_id'] = '_'

    date_time = sel.xpath('//meta[@name="publishdate"]/@content').extract_first()
    post_item['date_time'] = check_value(date_time)

    read_num = sel.xpath('//span[@class="readNum"]/text()').extract_first()
    post_item['read_num'] = check_value(read_num)

    reply_num = sel.xpath('//span[@class="replayNum"]/text()').extract_first()
    post_item['reply_num'] = check_value(reply_num)

    prise_num = sel.xpath('//span[contains(@class, "supportBtn")]/@overscore').extract_first()
    post_item['prise_num'] = check_value(prise_num)

    content_href = sel.xpath('//article/div[contains(@class, "article")]/@content_path').extract_first()
    post_item['content_href'] = check_value(content_href)

    post_item['comment_ids'] = []

    post_item['parse_time'] = time.time()

    return post_item


def get_post_content(response):
    text = response.text
    sel = Selector(text=text)

    content = sel.xpath('string(.)').extract_first()
    picture_hrefs = sel.xpath('//img/@src').extract()

    if picture_hrefs:
        picture_hrefs = [response.urljoin(pic_href) for pic_href in picture_hrefs]

    return check_value(content), picture_hrefs
