#!/usr/bin python3
# -*- coding: utf-8 -*-
import re

import time
from scrapy import Selector

from sohuBBSSpider.items import PostItem
from sohuBBSSpider.spiders.author import get_author_id_by_href
from sohuBBSSpider.spiders.post_list import get_post_list_div

check_value = lambda x: x if x else ''


def get_post_item(response):
    sel = Selector(response)
    url = response.url

    post_item = PostItem()
    post_item['url'] = url

    title = sel.xpath('//h3[@class="postitle"]/em[@class="title "]').xpath('string(.)').extract_first()
    post_item['title'] = check_value(title)

    post_id = get_id_by_post_href(url)

    post_item['post_id'] = check_value(post_id)

    read_div = sel.xpath('//span[@class="thread_reads"]/text()').extract_first()
    p_read = re.compile('阅读:(.*?) 回复: (.*)')
    post_item['read_num'] = '-1'
    post_item['reply_num'] = '-1'

    if read_div:
        try:
            read_s = p_read.search(read_div)
            if read_s:
                read_num = read_s.group(1)
                reply_num = read_s.group(2)
                post_item['read_num'] = check_value(read_num)
            post_item['reply_num'] = check_value(reply_num)
        except:
            pass

    tag_name = '#bbs_postlist'
    post_scripts = get_post_list_div(response, tag_name)

    if post_scripts:
        post_sel = Selector(text=post_scripts)
        post_div = post_sel.xpath('//*[@id="bbs_postlist"]/table[@id="post_0"]')

        content_text = post_div.xpath('./tr/td/div[@class="wrap"]/p').xpath('string(.)').extract()
        post_item['content'] = ''.join(content_text)

        date_time = post_div.xpath('./tr/td/div[@class="grey"]/text()').extract()[-1]

        post_item['date_time'] = ''

        if date_time:
            p_date = re.compile('发表于 (.*)$')
            try:
                date_s = p_date.search(date_time)
                if date_s:
                    post_item['date_time'] = check_value(date_s.group(1)).strip()
            except:
                pass

        picture_href = post_div.xpath('./tr/td/div[@class="wrap"]/p//img/@src').extract()
        post_item['picture_hrefs'] = [response.urljoin(pic_href) for pic_href in picture_href if picture_href]

        author_name = post_div.xpath('./tr/th/*[@id="userinfo"]/a').xpath('string(.)').extract_first()
        author_href = post_div.xpath('./tr/th/*[@id="userinfo"]/a/@href').extract_first()
        post_item['author_name'] = check_value(author_name)
        post_item['author_href'] = check_value(author_href)

        author_id = get_author_id_by_href(author_href)
        post_item['author_id'] = check_value(author_id)

        post_item['comment_ids'] = []

        parse_time = time.time()
        post_item['parse_time'] = str(parse_time)

        return post_item


def get_id_by_post_href(href):
    href_s = href.split('/')
    if href_s and len(href_s) > 5:
        return href_s[5]

    return None
