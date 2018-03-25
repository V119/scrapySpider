#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from kdnetSpider.items import CategoryItem

check_value = lambda x: x if x else ''


def get_category_list(response):
    """
    获取类别信息
    :param response:
    :return:
    """
    sel = Selector(response)
    info_list = sel.xpath('//table[contains(@id, "gb-forumlist") and not(@class)]/tr/td[2]/h2')
    for info in info_list:
        category_item = CategoryItem()
        cate_name = info.xpath('./span/a').xpath('string(.)').extract_first()
        category_item['name'] = check_value(cate_name)

        cate_url = info.xpath('./span/a/@href').extract_first()
        category_item['url'] = response.urljoin(cate_url)

        c_id = cate_url.split('?')[-1].split('=')[-1]
        category_item['id'] = check_value(c_id)

        today_num = info.xpath('./span[@class="c-alarm"]/text()').extract_first()
        category_item['today_num'] = check_value(today_num)

        num_span = info.xpath('./text()').extract()[-1]
        num_part = num_span.strip().split('/')
        comment_num = num_part[-2].strip().split('：')[-1].strip()
        topic_num = num_part[-1].strip().split('：')[-1][:-1].strip()
        category_item['comment_num'] = check_value(comment_num)
        category_item['topic_num'] = check_value(topic_num)
        category_item['parse_time'] = time.time()

        yield category_item


def get_last_cate_num():
    return None
    # 返回字典形式{类别ID:(回帖数， 主题数)}
