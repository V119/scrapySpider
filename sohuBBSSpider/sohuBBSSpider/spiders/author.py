#!/usr/bin python3
# -*- coding:utf-8 -*-
import time
from scrapy import Selector

from sohuBBSSpider.items import AuthorItem
from sohuBBSSpider.spiders.post_list import get_post_list_div

check_value = lambda x: x if x else ''


def get_author_item(response):
    url = response.url

    sel = Selector(response)

    author_item = AuthorItem()
    author_id = get_author_id_by_href(url)
    author_item['author_id'] = check_value(author_id)

    nick_name = sel.xpath('//div[@class="u_infocard u_basic"]/h3').xpath('string(.)').extract_first()
    author_item['nick_name'] = check_value(nick_name)

    sex = sel.xpath('//div[@class="u_infocard u_basic"]/div/span/text()').extract_first()
    author_item['sex'] = check_value(sex)

    introduction = sel.xpath('//div[@class="u_infocard u_basic"]/dl[@class="clear"]/dd/p/text()').extract_first()
    author_item['introduction'] = check_value(introduction)

    more_info_div = sel.xpath('//div[@class="u_detail"]/div/ul/li')
    for info in more_info_div:
        info_title = info.xpath('./b/text()').extract_first()
        info_content = info.xpath('./span/text()').extract_first()

        if '职务' in info_title:
            author_item['duty'] = check_value(info_content)
        elif '发帖总数' in info_title:
            author_item['post_num'] = check_value(info_content)
        elif '社区生日' in info_title:
            author_item['birthday'] = check_value(info_content)
        elif '上次登录' in info_title:
            author_item['last_login'] = check_value(info_content)
        elif '级别' in info_title:
            author_item['level'] = check_value(info_content)
        elif '精华贴数' in info_title:
            author_item['elite_num'] = check_value(info_content)
        elif '在线时间' in info_title:
            author_item['online_time'] = check_value(info_content)
        elif '上站次数' in info_title:
            author_item['login_num'] = check_value(info_content)
        elif '头衔' in info_title:
            author_item['title'] = check_value(info_content)
        elif '积分' in info_title:
            author_item['point'] = check_value(info_content)
        elif '声望魅力' in info_title:
            author_item['reputation'] = check_value(info_content)
        elif '喜欢的运动' in info_title:
            author_item['sport'] = check_value(info_content)
        elif '喜欢的电影' in info_title:
            author_item['movie'] = check_value(info_content)
        elif '喜欢的音乐' in info_title:
            author_item['music'] = check_value(info_content)
        elif '喜欢的美食' in info_title:
            author_item['food'] = check_value(info_content)
        elif '喜欢的书' in info_title:
            author_item['book'] = check_value(info_content)
        elif '喜欢的人' in info_title:
            author_item['person'] = check_value(info_content)
        elif '学历' in info_title:
            author_item['education'] = check_value(info_content)
        elif '职业' in info_title:
            author_item['profession'] = check_value(info_content)
        else:
            print('more info tag: ' + info_title)

    friends_num = get_post_list_div(response, '.friend_total_num')
    fans_num = get_post_list_div(response, '#fans_total_num')

    author_item['friends_num'] = check_value(friends_num)
    author_item['fans_num'] = check_value(fans_num)

    parse_time = time.time()
    author_item['parse_time'] = str(parse_time)

    return author_item


def get_author_id_by_href(href):
    href_s = href.split('?')
    if href_s and len(href_s) > 1:
        href_p = href_s[1].split('=')
        if href_p and len(href_p) > 1:
            return href_p[1]

    return None
