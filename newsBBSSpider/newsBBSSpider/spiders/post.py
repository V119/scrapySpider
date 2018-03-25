#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from newsBBSSpider.items import PostItem
from newsBBSSpider.spiders.author import gen_author_id

check_value = lambda x: x if x else ''


def get_post_item(response):
    url = response.url
    sel = Selector(response)

    post_item = PostItem()

    post_item['url'] = url

    post_id = sel.xpath('//input[@name="parentid"]/@value').extract_first()
    post_item['post_id'] = check_value(post_id)

    path_href = sel.xpath('//div[@class="de-nav"]/ul[@class="clear"]/li[not(@class)]/a/@href').extract()
    path_text = sel.xpath('//div[@class="de-nav"]/ul[@class="clear"]/li[not(@class)]/a/text()').extract()
    post_item['path_href'] = ', '.join([response.urljoin(href) for href in path_href if path_href])
    post_item['path_text'] = ', '.join(path_text)

    title = sel.xpath('//div[contains(@class, "de-zw")]/h1').xpath('string(.)').extract_first()
    post_item['title'] = check_value(title)

    author_url = sel.xpath('//ul[contains(@class, "de-xx")]/li[2]/a/@href').extract_first()
    post_item['author_url'] = response.urljoin(author_url) if author_url else ''

    author_text = sel.xpath('//ul[contains(@class, "de-xx")]/li[2]/a/text()').extract_first()
    post_item['author_name'] = check_value(author_text)

    author_id = gen_author_id(author_url)
    post_item['author_id'] = check_value(author_id)

    date_time = sel.xpath('//ul[contains(@class, "de-xx")]/li[@class="fr"]/span/text()').extract_first()
    post_item['date_time'] = check_value(date_time)

    read_num = sel.xpath('//ul[contains(@class, "de-xx")]/li[@class="fr ll"]/span/text()').extract_first()
    post_item['read_num'] = check_value(read_num)

    comment_num = sel.xpath('//ul[contains(@class, "de-xx")]/li[@class="fr pl"]/span/text()').extract_first()
    post_item['comment_num'] = check_value(comment_num)

    like_num = sel.xpath('//div[@class="de-zan"]/p').xpath('string(.)').extract_first()
    post_item['like_num'] = check_value(like_num)

    content_detail = sel.xpath('//div[@class="de-tai"]/p/a')
    post_item['detail_href'] = ''
    if content_detail:
        text = content_detail.xpath('./text()').extract_first()
        if text == '查看原文':
            detail_href = content_detail.xpath('./@href').extract_first()
            if detail_href:
                post_item['detail_href'] = check_value(detail_href)

    content = sel.xpath('//*[@id="message_"]').xpath('string(.)').extract_first()
    post_item['content'] = check_value(content)

    picture_href = sel.xpath('//*[@id="message_"]//img/@src').extract()
    post_item['picture_hrefs'] = picture_href

    post_item['parse_time'] = time.time()

    post_item['comment_ids'] = []

    return post_item

