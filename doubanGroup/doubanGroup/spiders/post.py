#!/usr/bin python3
# -*- coding:utf-8 -*-
from scrapy import Selector

from doubanGroup.items import PostItem
from doubanGroup.spiders.group import get_group_id_by_href

check_value = lambda x: x if x else ''


def get_post_item(response):
    url = response.url

    sel = Selector(response)
    post_item = PostItem()
    post_item['url'] = url

    post_id = sel.xpath('//div[@class="sns-bar-fav"]/a/@data-tid').extract_first()
    post_item['post_id'] = check_value(post_id)

    group_name = sel.xpath('//div[@class="group-item"]/div[@class="info"]/div[@class="title"]/a/text()').extract_first()
    post_item['group_name'] = check_value(group_name)

    group_href = sel.xpath('//div[@class="group-item"]/div[@class="info"]/div[@class="title"]/a/@href').extract_first()
    post_item['group_href'] = check_value(group_href)

    group_id = get_group_id_by_href(group_href)
    post_item['group_id'] = check_value(group_id)

    pic_src = sel.xpath('//div[@class="user-face"]/a/img[@class="pil"]/@src').extract_first()
    post_item['author_id'] = get_author_id_by_head_src(pic_src)

    author_name = sel.xpath('//span[@class="from"]/a/text()').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_href = sel.xpath('//span[@class="from"]/a/@href').extract_first()
    post_item['author_href'] = check_value(author_href)

    title = sel.xpath('//div[@id="content"]/h1/text()').extract_first()
    post_item['title'] = check_value(title).strip()

    date_time = sel.xpath('//span[@class="color-green"]/text()').extract_first()
    post_item['date_time'] = check_value(date_time)

    content = sel.xpath('//div[@id="link-report"]/div[@class="topic-content"]').xpath('string(.)').extract_first()
    post_item['content'] = check_value(content)

    picture_hrefs = sel.xpath('//div[@id="link-report"]/div[@class="topic-content"]//img/@src').extract()
    post_item['picture_hrefs'] = [response.urljoin(pic_href) for pic_href in picture_hrefs if pic_href]

    recommend_num = sel.xpath('//div[@class="rec-sec"]/span[@class="rec-num"]/text()').extract_first()
    if recommend_num and len(recommend_num) > 1:
        post_item['recommend_num'] = recommend_num[:-1]
    else:
        post_item['recommend_num'] = '0'

    like_num = sel.xpath('//div[@class="sns-bar-fav"]/span[@class="fav-num"]/a/text()').extract_first()
    if like_num and len(like_num) > 1:
        post_item['like_num'] = like_num[:-1]
    else:
        post_item['like_num'] = '0'

    post_item['comment_ids'] = []

    return post_item


def get_author_id_by_head_src(pic_src):
    pic_name = pic_src.split('/')[-1]

    author_id = '_'
    if pic_name:
        u_id = pic_name.split('-')[0]
        if u_id:
            author_id = u_id[1:]

    return author_id
