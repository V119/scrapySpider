#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from hbase.ttypes import *

from sanqinSpider.utils import MD5Utils


def gen_start_spider_info():
    """
    在爬虫开始时记录爬虫开始的时间
    :return:
    """
    now = time.time()
    spider_name = 'sanqin_news'
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
    spider_name = 'moe_gov'

    name_column = TColumnValue(b'spider_name', b'name', spider_name.encode())
    time_column = TColumnValue(b'time', b'stop_time', str(now).encode())
    column_values = [name_column, time_column]
    put = TPut(row_key, column_values)

    return put


def gen_news_put(news_item):
    """
    产生文件公告的插入数据库的数据
    :param news_item:
    :return: rowKey
             put
    """
    info_fml = b'info'
    file_picture_fml = b'pictures'

    url = news_item['url']
    publish_time = news_item['publish_time']
    row_key = gen_row_key(MD5Utils.md5_code(publish_time), MD5Utils.md5_code(url))

    column_values = []

    # blogInfo 列族的信息
    url_column = TColumnValue(info_fml, b'url', str(url).encode())
    column_values.append(url_column)

    path_url_column = TColumnValue(info_fml, b'path_url', str(news_item['path_url']).encode())
    column_values.append(path_url_column)

    path_text_column = TColumnValue(info_fml, b'path_text', str(news_item['path_text']).encode())
    column_values.append(path_text_column)

    title_column = TColumnValue(info_fml, b'title', str(news_item['title']).encode())
    column_values.append(title_column)

    publish_time_column = TColumnValue(info_fml, b'publish_time', str(news_item['publish_time']).encode())
    column_values.append(publish_time_column)

    editor_column = TColumnValue(info_fml, b'editor', str(news_item['editor']).encode())
    column_values.append(editor_column)

    abstract_column = TColumnValue(info_fml, b'abstract', str(news_item['abstract']).encode())
    column_values.append(abstract_column)

    source_text_column = TColumnValue(info_fml, b'source_text', str(news_item['source_text']).encode())
    column_values.append(source_text_column)

    source_href_column = TColumnValue(info_fml, b'source_href', str(news_item['source_href']).encode())
    column_values.append(source_href_column)

    picture_urls_column = TColumnValue(info_fml, b'picture_urls', str(news_item['picture_urls']).encode())
    column_values.append(picture_urls_column)

    content_column = TColumnValue(info_fml, b'content', str(news_item['content']).encode())
    column_values.append(content_column)

    key_words_column = TColumnValue(info_fml, b'key_words', str(news_item['key_words']).encode())
    column_values.append(key_words_column)

    b_files = news_item['b_pictures']

    b_file_num = len(b_files)
    b_file_column = TColumnValue(file_picture_fml, b'file_num', str(b_file_num).encode())
    column_values.append(b_file_column)

    for file_url in b_files.keys():
        b_file = b_files[file_url]
        column_values.append(TColumnValue(file_picture_fml, MD5Utils.md5_code(file_url).encode(), b_file))

    put = TPut(row_key, column_values)

    return row_key, put


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
