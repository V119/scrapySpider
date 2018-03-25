#!/bin/usr python3
# -*- coding: utf-8 -*-
import json

from scrapy import Selector

from sinaBlogSpider.items import CommentItem

check_value = lambda x: x if x else ''


def get_comment_info(response, post_id):
    body = response.text

    o = json.loads(body)

    data = o['data']
    comment_item_list = []
    if data and 'comment_data' in data:
        comment_list = data['comment_data']
        for comment_data in comment_list:
            comment_item = CommentItem()
            comment_item['post_id'] = post_id

            comment_id = comment_data.get('id')
            comment_item['comment_id'] = check_value(comment_id)

            author_id = comment_data.get('comm_uid')
            comment_item['author_id'] = check_value(author_id)

            author_name = comment_data.get('uname')
            comment_item['author_name'] = check_value(author_name)

            author_href = comment_data.get('ulink')
            comment_item['author_href'] = check_value(author_href)

            content = comment_data.get('cms_body')
            comment_item['content'] = check_value(content)

            date_time = comment_data.get('cms_pubdate')
            comment_item['date_time'] = check_value(date_time)

            replay_num = comment_data.get('cms_reply_num')
            comment_item['replay_num'] = check_value(replay_num)

            comment_item_list.append(comment_item)

    comment_num = data['comment_num']

    return comment_item_list, comment_num


def get_comment_ajax(post_id, page=1):
    href = 'http://blog.sina.com.cn/s/comment_' + post_id + '_' + str(page) \
           + '.html?comment_v=articlenew'

    return href
