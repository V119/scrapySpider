#!/usr/bin python3
# -*- coding: utf-8 -*-
import json


def get_fans_url(user_id, page_num):
    url = 'http://www.tianya.cn/api/tw?method=follower.ice.select&params.userId=' \
          + user_id + '&params.pageNo=' + str(page_num) + '&params.pageSize=28'

    return url


def get_friends_url(user_id, page_num):
    url = 'http://www.tianya.cn/api/tw?method=following.ice.select&params.userId=' \
          + user_id + '&params.pageNo=' + str(page_num) + '&params.pageSize=28'

    return url


def get_fans_user_id_list(response):
    body = response.text
    id_list = []
    try:
        json_obj = json.loads(body)
        if json_obj:
            code = json_obj['code']
            if '1' == code:
                user_list = json_obj['data']['user']
                for user_info in user_list:
                    user_id = user_info['id']
                    id_list.append(user_id)
    finally:
        return id_list

