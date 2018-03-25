#!/usr/bin python3
# -*- coding:utf-8 -*-
import json

from scrapy import Selector

from chinaBBSSpider.items import CommentItem


def get_comment_url(response, page_num=1):
    sel = Selector(response)

    forum_id = sel.re(r'var\s+forumid\s*=\s*(.*);')[0]
    thread_id = sel.re(r'var\s+threadid\s*=\s*(.*);')[0]

    thread_list = [thread_id[:-5], thread_id[-5:-3], thread_id[-3:-1], thread_id[-1:]]
    thread_path = '/'.join(thread_list)

    comment_href = 'http://st01.club.china.com/data/thread/' \
                   + forum_id + '/' + thread_path + '_' + str(page_num) + '_re.js'

    return comment_href


def get_comment_list(response, post_id):
    sel = Selector(response)
    # noinspection PyBroadException
    try:
        comment_json = sel.re(r'page_obj\s*=\s*(.*);\s*printReCallBack')[0]
    except:
        comment_json = None
        print('comment page error:  ' + response.url)

    if comment_json:
        # noinspection PyBroadException
        try:
            comment_obj = json.loads(comment_json
                                     .replace('"%5C%22', '\\"')
                                     .replace('%5C%22"', '\\"')
                                     .replace('"\\', "")
                                     .replace(';" src=', ';\\" src=')
                                     .replace('onerror="', "onerror='"))
            if comment_obj:
                comment_list = comment_obj['l']
                for comment in comment_list:
                    comment_item = CommentItem()
                    comment_item['post_id'] = post_id
                    comment_item['comment_id'] = comment['mi']
                    comment_item['author_id'] = comment['ui']
                    comment_item['author_name'] = comment['nc']

                    comment_item['date_time'] = comment['cd']
                    comment_item['floor'] = comment['lc']
                    comment_item['content'] = comment['nr']

                    yield comment_item
        except:
            print('json: ' + comment_json + '   error!!')


def get_comment_prise(response):
    sel = Selector(response)

    prise_json = sel.re(r'var\s+dingJson\s*=\s*(.*);')[0]

    json_obj = json.loads(
        ('{"l":' + prise_json + '}')
            .replace('messageid', '"messageid"')
            .replace('ding', '"ding"')
            .replace('\'', '"'))

    prise_list = json_obj['l']
    prise_dict = {}
    for prise in prise_list:
        prise_dict[prise['messageid']] = prise['ding']

    return prise_dict


