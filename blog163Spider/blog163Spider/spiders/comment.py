#!/usr/bin python3
# -*- coding:utf-8 -*-
import uuid

import time
from scrapy import Selector

from blog163Spider.items import CommentItem
from blog163Spider.spiders.author import get_author_by_href

check_value = lambda x: x if x else ''


def get_comment_item(response, post_id):
    sel = Selector(response)

    comment_div_list = sel.xpath('//div[@class="case"]/div[contains(@class, "nbw-cmt bdwbd")]')
    for comment_div in comment_div_list:
        comment_item = CommentItem()

        comment_id = str(uuid.uuid1())
        comment_item['comment_id'] = comment_id

        comment_item['post_id'] = check_value(post_id)

        get_div_info(comment_div, comment_item)

        child_div_list = comment_div.xpath('./div[@class="thde"]/div[@class="reps atag"]/div[@class="nbw-cmt bdwt"]')
        child_comment_ids = []
        for child_div in child_div_list:
            comment_child_item = CommentItem()
            comment_child_item['post_id'] = post_id
            comment_child_item['replay_comment_id'] = comment_id
            get_div_info(child_div, comment_child_item)
            child_comment_ids.append(comment_id)

            yield comment_child_item

        yield comment_item


def get_div_info(comment_div, comment_item):
    author_name = comment_div.xpath('./div[@class="thde"]/div[@class="tt"]'
                                    '/div[@class="tx atag"]/a').xpath('string(.)').extract_first()
    comment_item['author_name'] = check_value(author_name)

    author_href = comment_div.xpath('./div[@class="thde"]/div[@class="tt"]'
                                    '/div[@class="tx atag"]/a/@href').extract_first()
    comment_item['author_href'] = check_value(author_href)

    author_id = get_author_by_href(author_href)
    comment_item['author_id'] = check_value(author_id)

    content = comment_div.xpath('./div[@class="thde"]/div[@class="cnt pre atag"]/') \
        .xpath('string(.)').extract_first()
    comment_item['content'] = check_value(content)

    date_time = comment_div.xpath('./div[@class="thde"]/div[@class="tt"]'
                                  '/span[@class="pright fc07 atag"]').xpath('string(.)').extract_first()
    comment_item['date_time'] = check_value(date_time)

    parse_time = time.time()
    comment_item['parse_time'] = parse_time
