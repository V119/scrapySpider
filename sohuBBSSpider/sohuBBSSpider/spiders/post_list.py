#!/usr/bin python3
# -*- coding: utf-8 -*-
import json
import re

from scrapy import Selector


def get_post_author_list(response):
    tag_name = '#bbs_list'
    div_text = get_post_list_div(response, tag_name)
    post_authors_list = []

    if div_text:
        sel = Selector(text=div_text)
        post_list = sel.xpath('//table[@class="postlist"]/tr')
        for post in post_list:
            post_href = post.xpath('./td[@class="posttitle"]/a/@href').extract_first()
            author_hrefs = post.xpath('./td/span/a/@href').extract()
            if post_href:
                post_authors_list.append((response.urljoin(post_href),
                                          [response.urljoin(a_l) for a_l in set(author_hrefs)]))

    return post_authors_list


def get_next_page_url(response):
    tag_name = '#bbs_list'
    div_text = get_post_list_div(response, tag_name)
    if div_text:
        sel = Selector(text=div_text)
        page_div = sel.xpath('//div[@class="pages"]/span/a')
        for page in page_div:
            page_text = page.xpath('./text()').extract_first()
            if '下一页' in page_text:
                page_href = page.xpath('./@href').extract_first()
                return response.urljoin(page_href)
    pass


def get_post_list_div(response, tag_name):
    sel = Selector(response)

    script_divs = sel.xpath('//script/text()').extract()
    for script_div in script_divs:
        p = re.compile('club\.render\.fill\((.*)\)')

        script_text = None
        try:
            script_s = p.search(script_div)
            if script_s:
                script_text = script_s.group(1)
        except Exception as e:
            print('解析script出错' + e)

        if script_text:
            # noinspection PyBroadException
            try:
                script_obj = json.loads(script_text)
                if script_obj and 'tag' in script_obj:
                    if script_obj['tag'] == tag_name:
                        return script_obj['content']
            except:
                pass

    return None
