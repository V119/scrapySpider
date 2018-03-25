#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from sohuBBSSpider.spiders.post_list import get_post_list_div


def get_user_list(response, fans_or_friends_tag):
    body_text = get_post_list_div(response, fans_or_friends_tag)
    sel = Selector(text=body_text)

    user_list = sel.xpath('//div[@class="u_tab_content"]/dl')
    user_info_list = []
    for user in user_list:
        user_href = user.xpath('./dd/div[@class="fans_info"]/a/@href').extract_first()
        user_id = user.xpath('./dd/div[@class="fans_info"]/a/@action_data').extract_first()

        if user_href:
            user_info_list.append((user_id, response.urljoin(user_href)))

    return user_info_list


def get_user_next_page(response, tag_name):
    body_text = get_post_list_div(response, tag_name)
    sel = Selector(text=body_text)

    page_list = sel.xpath('//div[@class="pages"]/span/a')
    for page in page_list:
        page_text = page.xpath('./text()').extract_first()
        if '下一页' in page_text:
            page_href = page.xpath('./@href').extract_first()
            if page_href:
                return response.urljoin(page_href)

    return None
