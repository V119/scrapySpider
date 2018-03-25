#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from sinaBlogSpider.items import AuthorItem

check_value = lambda x: x if x else ''


def get_author_info(response):
    sel = Selector(response)

    author_item = AuthorItem()

    url = response.url
    author_item['url'] = url

    author_id = get_author_id_by_url(url)
    author_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//*[@id="ownernick"]').xpath('string(.)').extract_first()
    author_item['author_name'] = check_value(author_name).strip()

    pic_head_url = sel.xpath('//div[@class="info"]/div[@class="info_img"]/img/@src').extract_first()
    author_item['picture_head_url'] = check_value(pic_head_url)

    level_pic = sel.xpath('//span[contains(@id, "grade")]/img/@src').extract()
    level_num = [pic[-5] for pic in level_pic]
    author_item['level'] = ''.join(level_num) if level_num else '-1'

    point = sel.xpath('//span[contains(@id, "score")]/a').xpath('string(.)').extract_first()
    author_item['point'] = check_value(point)

    visit_num = sel.xpath('//span[contains(@id, "pv")]').xpath('string(.)').extract_first()
    author_item['visit_num'] = check_value(visit_num)

    popularity = sel.xpath('//span[contains(@id, "attention")]').xpath('string(.)').extract_first()
    author_item['popularity'] = check_value(popularity)

    get_golden = sel.xpath('//span[contains(@id, "d_goldpen")]').xpath('string(.)').extract_first()
    author_item['get_golden'] = check_value(get_golden)

    give_golden = sel.xpath('//span[contains(@id, "r_goldpen")]').xpath('string(.)').extract_first()
    author_item['give_golden'] = check_value(give_golden)

    author_records = sel.xpath('//div[contains(@class, "component")]/div[contains(@class, "basicInfo")]')
    author_item['info'] = check_value(author_records[0].xpath('string(.)').extract_first())
    author_item['experience'] = check_value(author_records[1].xpath('string(.)').extract_first())
    author_item['introduction'] = check_value(author_records[2].xpath('string(.)').extract_first())
    author_item['certification'] = check_value(author_records[3].xpath('string(.)').extract_first())

    return author_item


def get_author_id_by_url(author_url):
    """
    根据用户主页url获取用户ID
    :param author_url:
    :return:
    """
    url_split = author_url.split('_')
    if url_split and len(url_split) > 1:
        author_id = url_split[-1].strip()[:-5]

        return author_id

    return None

