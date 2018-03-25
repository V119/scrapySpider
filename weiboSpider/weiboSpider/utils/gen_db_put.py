# #!/usr/bin python3
# # -*- coding: utf-8 -*-
# import time
# from hbase.ttypes import *
#
# from xinhuaNewsSpider.utils import MD5Utils
#
#
# def gen_start_spider_info():
#     """
#     在爬虫开始时记录爬虫开始的时间
#     :return:
#     """
#     now = time.time()
#     spider_name = 'xinhuaNews'
#     # 让最新的行放在最前面
#     row_key = gen_row_key(MD5Utils.md5_code(spider_name), str(10 ** 12 - now))
#
#     name_column = TColumnValue(b'spider_name', b'name', spider_name.encode())
#     time_column = TColumnValue(b'time', b'start_time', str(now).encode())
#     column_values = [name_column, time_column]
#     put = TPut(row_key, column_values)
#
#     return row_key, put
#
#
# def gen_stop_spider_info(row_key):
#     """
#     在爬虫结束时，记录爬虫结束的时间
#     :param row_key:
#     :return:
#     """
#     now = time.time()
#     spider_name = 'xinhuaNews'
#
#     name_column = TColumnValue(b'spider_name', b'name', spider_name.encode())
#     time_column = TColumnValue(b'time', b'stop_time', str(now).encode())
#     column_values = [name_column, time_column]
#     put = TPut(row_key, column_values)
#
#     return put
#
#
# def gen_news_put(news_item):
#     """
#     产生插入数据库的PUT
#     :param news_item:
#     :return: rowKey
#              put
#     """
#     info_fml = b'info'
#     picture_fml = b'pictures'
#
#     url = news_item['url']
#     date_time = news_item['date_time']
#     if not date_time:
#         date_time = '0000年00月00日'
#
#     row_key = gen_row_key(MD5Utils.md5_code(date_time), MD5Utils.md5_code(url))
#
#     column_values = []
#
#     # blogInfo 列族的信息
#     url_column = TColumnValue(info_fml, b'url', str(url).encode())
#     column_values.append(url_column)
#
#     key_words_column = TColumnValue(info_fml, b'key_words', str(news_item['key_words']).encode())
#     column_values.append(key_words_column)
#
#     path_href_column = TColumnValue(info_fml, b'path_href', str(news_item['path_href']).encode())
#     column_values.append(path_href_column)
#
#     path_text_column = TColumnValue(info_fml, b'path_text', str(news_item['path_text']).encode())
#     column_values.append(path_text_column)
#
#     title_column = TColumnValue(info_fml, b'title', str(news_item['title']).encode())
#     column_values.append(title_column)
#
#     publish_time_column = TColumnValue(info_fml, b'date_time', str(news_item['date_time']).encode())
#     column_values.append(publish_time_column)
#
#     source_text_column = TColumnValue(info_fml, b'source_text', str(news_item['source']).encode())
#     column_values.append(source_text_column)
#
#     picture_urls_column = TColumnValue(info_fml, b'picture_urls', str(news_item['picture_urls']).encode())
#     column_values.append(picture_urls_column)
#
#     content_column = TColumnValue(info_fml, b'content', str(news_item['content']).encode())
#     column_values.append(content_column)
#
#     editor_column = TColumnValue(info_fml, b'editor', str(news_item['editor']).encode())
#     column_values.append(editor_column)
#
#     if 'author' in news_item.fields:
#         author_column = TColumnValue(info_fml, b'author', str(news_item['author']).encode())
#         column_values.append(author_column)
#
#     b_pictures = news_item['b_pictures']
#
#     b_picture_num = len(b_pictures)
#     b_file_column = TColumnValue(picture_fml, b'pic_num', str(b_picture_num).encode())
#     column_values.append(b_file_column)
#
#     for x in range(b_picture_num):
#         column_values.append(TColumnValue(picture_fml, str(x).encode(), b_pictures[x]))
#
#     put = TPut(row_key, column_values)
#
#     return row_key, put
#
#
# def gen_row_key(*strs):
#     """
#     用下划线'_'拼接字符串，以产生rowKey
#     :param strs:
#     :return:
#     """
#     if not strs:
#         raise ValueError('产生rowKey传递的参数不能为空!!!')
#
#     result = ''
#     for s in strs:
#         result = result + s + '_'
#
#     return result[:-1].encode()
