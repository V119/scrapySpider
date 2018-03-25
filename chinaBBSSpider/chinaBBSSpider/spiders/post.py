#!/usr/bin python3
# -*- coding: utf-8 -*-
import re
import time
from scrapy import Selector

from chinaBBSSpider.items import PostItem

check_value = lambda x: x if x else ''


def get_post_item(response):
    url = response.url
    sel = Selector(response)

    post_item = PostItem()
    post_item['url'] = url

    forum_id = sel.re(r'var\s+forumid\s*=\s*(.*);')[0]
    thread_id = sel.re(r'var\s+threadid\s*=\s*(.*);')[0]

    post_item['post_id'] = forum_id + '_' + thread_id

    path_text = sel.xpath('//div[contains(@class, "breadcrumbs")]/a/text()').extract()
    path_href = sel.xpath('//div[contains(@class, "breadcrumbs")]/a/@href').extract()
    post_item['path_text'] = ', '.join(path_text)
    post_item['path_href'] = ', '.join([response.urljoin(p_href) for p_href in path_href if p_href])

    title = sel.xpath('//*[@id="chan_newsTitle"]').xpath('string(.)').extract_first()
    post_item['title'] = check_value(title)

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    post_item['key_words'] = check_value(key_words)

    hot_words = sel.xpath('//div[@class="hotWords"]/a/text()').extract()
    post_item['hot_words'] = ', '.join(hot_words)

    author_id = sel.xpath('//span[@class="author"]/a[@name="onlineIcon"]/@_webim_ppid').extract_first()
    post_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//span[@class="author"]/a/text()').extract_first()
    post_item['author_name'] = check_value(author_name)

    level = sel.xpath('//span[@class="level"]/img/@title').extract_first()
    post_item['level'] = check_value(level)

    point = sel.xpath('//div[@class="grade"]/span[not(@class)]/text()').extract_first()
    if point and len(point) > 3:
        post_item['point'] = point[3:]
    else:
        post_item['point'] = ''

    date_time = sel.xpath('//li[@class="time"]/span/text()').extract_first()
    if date_time and len(date_time) > 4:
        post_item['date_time'] = date_time[4:]
    else:
        post_item['date_time'] = ''

    num_href = sel.xpath('//div[@class="postStaticData"]/span/script/@src').extract_first()
    post_item['_num_href'] = check_value(num_href)

    content, picture_hrefs = get_content(response)
    post_item['content'] = check_value(content)
    post_item['picture_hrefs'] = picture_hrefs

    post_item['comment_ids'] = []

    post_item['parse_time'] = time.time()

    return post_item


def parse_num_js(response):
    text = response.text

    read_p = re.compile(r'r_hits\s*=\s*(.*?);')
    participant_p = re.compile(r'r_joins\s*=\s*(.*?);')
    reply_p = re.compile(r'r_re\s*=\s*(.*?);')

    read_num = read_p.search(text).group(1)
    participant_num = participant_p.search(text).group(1)
    reply_num = reply_p.search(text).group(1)

    return check_value(read_num), check_value(participant_num), check_value(reply_num)


def get_content(response):
    sel = Selector(response)

    content = sel.xpath('//div[@id="chan_newsDetail"]').xpath('string(.)').extract_first()
    picture_hrefs = sel.xpath('//div[@id="chan_newsDetail"]//img/@src').extract()

    return check_value(content), [response.urljoin(p_href) for p_href in picture_hrefs if p_href]


def get_post_next_page(response):
    sel = Selector(response)

    next_page = sel.xpath('//*[@id="chan_multipageNumN"]/a[@class="nextPage"]/@href').extract_first()

    return next_page

