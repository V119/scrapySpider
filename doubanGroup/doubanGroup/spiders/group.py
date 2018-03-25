#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from doubanGroup.items import GroupItem
from doubanGroup.utils.MD5Utils import md5_code

check_value = lambda x: x if x else ''


def get_group_item(response):
    url = response.url
    sel = Selector(response)

    group_item = GroupItem()
    group_item['url'] = url

    group_id = get_group_id_by_href(url)
    group_item['group_id'] = group_id

    group_name = sel.xpath('//div[@id="group-info"]/h1/text()').extract_first()
    group_item['group_name'] = check_value(group_name).strip()

    create_time_line = sel.xpath('//div[@class="group-board"]/p/text()').extract_first()
    group_item['create_time'] = ''
    if create_time_line:
        create_time = create_time_line.strip().split(' ')[0]
        if create_time and len(create_time.strip()) > 12:
            group_item['create_time'] = create_time[3:]

    leader_name = sel.xpath('//div[@class="group-board"]/p/a/text()').extract_first()
    group_item['leader_name'] = check_value(leader_name)

    leader_href = sel.xpath('//div[@class="group-board"]/p/a/@href').extract_first()
    group_item['leader_href'] = check_value(leader_href)

    content = sel.xpath('//div[@class="group-board"]/div[@class="group-intro"]').xpath('string(.)').extract_first()
    group_item['content'] = check_value(content)

    group_tags = sel.xpath('//div[@class="group-tags"]/a/text()').extract()
    group_item['group_tags'] = ', '.join(group_tags)

    return group_item


def get_group_id_by_href(o_href):
    href = o_href.split('?ref=')[0]
    group_id = md5_code(href)

    return group_id
