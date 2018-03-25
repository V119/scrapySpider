#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from xinwen110Spider.items import NewsItem

check_value = lambda x: x if x else ''


def get_news_info(response):
    sel = Selector(response)
    item = NewsItem()
    url = response.url

    item['url'] = url

    # 路径
    path_xpath = '//div[@class="t2"]/a'
    path_text, path_href = get_path_info(response, path_xpath)
    item['path_text'] = check_value(path_text).strip()
    item['path_href'] = check_value(path_href).strip()

    # 标题
    title = sel.xpath('//div[@class="main_title"]').xpath('string(.)').extract_first()
    item['title'] = title

    # 日期时间
    info_div = sel.xpath('//div[@class="top_about"]/a')
    date_time = info_div[0].xpath('string(.)').extract_first()
    source = info_div[1].xpath('string(.)').extract_first()

    item['date_time'] = check_value(date_time).strip()
    item['source'] = check_value(source).strip()

    # 浏览量
    read_num = sel.xpath('//*[@id="hits"]').xpath('string(.)').extract_first()
    comment_num = sel.xpath('//*[@id="commnetsnum"]').xpath('string(.)').extract_first()

    item['read_num'] = check_value(read_num).strip()
    item['comment_num'] = check_value(comment_num).strip()

    # 内容
    content = sel.xpath('//*[@id="zoom"]').xpath('string(.)').extract_first()
    item['content'] = check_value(content).strip()

    # 图片
    picture_urls = sel.xpath('//*[@id="zoom"]//img/@src').extract()
    item['picture_url'] = [response.urljoin(pic_url) for pic_url in picture_urls if pic_url]

    return item


def get_path_info(response, path_xpath):
    sel = Selector(response)
    path_div = sel.xpath(path_xpath)

    path_text_list = []
    path_href_list = []
    for path in path_div:
        path_text = path.xpath('string(.)').extract_first()
        path_href = path.xpath('./@href').extract_first()
        path_text_list.append(check_value(path_text))
        path_href_list.append(response.urljoin(path_href))

    return '; '.join(path_text_list), '; '.join(path_href_list)
