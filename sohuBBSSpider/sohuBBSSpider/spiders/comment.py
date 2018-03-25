#!/usr/bin python3
# -*- coding: utf-8 -*-
import re

import time
from scrapy import Selector

from sohuBBSSpider.items import CommentItem
from sohuBBSSpider.spiders.author import get_author_id_by_href
from sohuBBSSpider.spiders.post import get_id_by_post_href
from sohuBBSSpider.spiders.post_list import get_post_list_div

check_value = lambda x: x if x else ''


def get_comment_items(response):
    url = response.url
    post_id = get_id_by_post_href(url)

    tag_name = '#bbs_postlist'
    post_scripts = get_post_list_div(response, tag_name)

    if post_scripts:
        post_sel = Selector(text=post_scripts)
        post_div = post_sel.xpath('//*[@id="bbs_postlist"]/table[contains(@id, "post_") and not(@id="post_0")]')
        for comment_script in post_div:
            comment_item = CommentItem()
            comment_item['post_id'] = check_value(post_id)

            floor_id = comment_script.xpath('./@id').extract_first()
            floor = floor_id.split('_')[-1]
            comment_item['floor'] = floor

            comment_item['comment_id'] = post_id + '_' + floor
            author_name = comment_script.xpath('./tr/th/*[@id="userinfo"]/a').xpath('string(.)').extract_first()
            author_href = comment_script.xpath('./tr/th/*[@id="userinfo"]/a/@href').extract_first()
            comment_item['author_name'] = check_value(author_name)
            comment_item['author_href'] = check_value(author_href)

            author_id = get_author_id_by_href(author_href)
            comment_item['author_id'] = check_value(author_id)

            content_text = comment_script.xpath('./tr/td/div[@class="wrap"]').xpath('string(.)').extract()
            comment_item['content'] = ''.join(content_text)

            date_time = comment_script.xpath('./tr/td/div[@class="grey"]'
                                             '/span[@class="new_format"]/text()').extract_first()

            comment_item['date_time'] = check_value(date_time)

            picture_href = comment_script.xpath('./tr/td/div[@class="wrap"]/p//img/@src').extract()
            comment_item['picture_hrefs'] = [response.urljoin(pic_href) for pic_href in picture_href if picture_href]

            quote_href = comment_script.xpath('./tr/td/div[@class="wrap"]/dl[@class="quote"]'
                                              '//span[@class="fright"]/a/@href').extract_first()
            comment_item['quote_floor'] = '0'
            if quote_href:
                quote_floor = quote_href.split('#')
                if quote_floor and len(quote_floor) > 1:
                    comment_item['quote_floor'] = check_value(quote_floor.split('_')[-1])

            parse_time = time.time()
            comment_item['parse_time'] = str(parse_time)

            yield comment_item


def get_comment_next_page_url(response):
    tag_name = '#bbs_postlist'
    script_div = get_post_list_div(response, tag_name)
    page_sel = Selector(text=script_div)
    page_div = page_sel.xpath('//div[@class="pages"]/span/a')
    for page in page_div:
        page_text = page.xpath('./text()').extract_first()
        if '下一页' in page_text:
            page_href = page.xpath('./@href').extract_first()
            if page_href:
                return response.urljoin(page_href)

    return None
