#!/usr/bin python3
# -*- coding:utf-8 -*-
import time

from doubanGroup.utils import MD5Utils

from hbase.ttypes import *


def gen_start_spider_info():
    """
    在爬虫开始时记录爬虫开始的时间
    :return:
    """
    now = time.time()
    spider_name = 'douban_group'
    # 让最新的行放在最前面
    row_key = gen_row_key(MD5Utils.md5_code(spider_name), str(10 ** 12 - now))

    name_column = TColumnValue(b'spider_name', b'name', spider_name.encode())
    time_column = TColumnValue(b'time', b'start_time', str(now).encode())
    column_values = [name_column, time_column]
    put = TPut(row_key, column_values)

    return row_key, put


def gen_stop_spider_info(row_key):
    """
    在爬虫结束时，记录爬虫结束的时间
    :param row_key:
    :return:
    """
    now = time.time()
    spider_name = 'douban_group'

    name_column = TColumnValue(b'spider_name', b'name', spider_name.encode())
    time_column = TColumnValue(b'time', b'stop_time', str(now).encode())
    column_values = [name_column, time_column]
    put = TPut(row_key, column_values)

    return put


def gen_row_key(*strs):
    """
    用下划线'_'拼接字符串，以产生rowKey
    :param strs:
    :return:
    """
    if not strs:
        raise ValueError('产生rowKey传递的参数不能为空!!!')

    result = ''
    for s in strs:
        result = result + s + '_'

    return result[:-1].encode()


def gen_post_put(post_item):
    """
    产生插入post数据库的put
    :param post_item:
    :return:
    """
    info_fml = b'info'
    picture_fml = b'picture'

    post_id = post_item['post_id']
    author_id = post_item['author_id']
    group_id = post_item['group_id']

    row_key = gen_row_key(MD5Utils.md5_code(author_id), MD5Utils.md5_code(group_id), MD5Utils.md5_code(post_id))

    column_values = []

    for key in post_item:
        if not key.startswith(('_', 'picture')):
            column_values.append(TColumnValue(info_fml, key.encode(), str(post_item[key]).encode()))
        elif key.startswith('picture'):
            column_values.append(TColumnValue(picture_fml, (key + '_num').encode(), str(len(post_item[key])).encode()))
            for p in range(len(post_item[key])):
                column_values.append(
                    TColumnValue(picture_fml, (key + str(p)).encode(), str(post_item[key][p]).encode()))

    put = TPut(row_key, column_values)

    return row_key, put


def gen_author_put(author_item):
    """
    产生插入author数据库的put
    :param author_item:
    :return:
    """
    info_fml = b'info'

    author_id = author_item['author_id']

    row_key = MD5Utils.md5_code(author_id).encode()

    column_values = []

    for key in author_item:
        column_values.append(TColumnValue(info_fml, key.encode(), str(author_item[key]).encode()))

    put = TPut(row_key, column_values)

    return row_key, put


def gen_comment_put(comment_item):
    """
    产生插入comment数据库的put
    :param comment_item:
    :return:
    """
    info_fml = b'info'

    comment_id = comment_item['comment_id']
    post_id = comment_item['post_id']

    row_key = gen_row_key(MD5Utils.md5_code(post_id), MD5Utils.md5_code(comment_id))

    column_values = []

    for key in comment_item:
        column_values.append(TColumnValue(info_fml, key.encode(), str(comment_item[key]).encode()))

    put = TPut(row_key, column_values)

    return row_key, put


def gen_group_put(group_item):
    """
    产生插入group数据库的put
    :param group_item:
    :return:
    """
    info_fml = b'info'
    group_id = group_item['group_id']

    row_key = gen_row_key(MD5Utils.md5_code(group_id))

    column_values = []

    for key in group_item:
        column_values.append(TColumnValue(info_fml, key.encode(), str(group_item[key]).encode()))

    put = TPut(row_key, column_values)

    return row_key, put


def gen_fans_put(fans_item):
    info_fml = b'info'

    fans_id = fans_item['fans_id']
    friends_id = fans_item['friends_id']

    row_key = gen_row_key(MD5Utils.md5_code(fans_id), MD5Utils.md5_code(friends_id))

    column_values = [TColumnValue(info_fml, b'fans_id', str(fans_item['fans_id']).encode()),
                     TColumnValue(info_fml, b'friends_id', str(fans_item['friends_id']).encode())]

    put = TPut(row_key, column_values)

    return row_key, put
