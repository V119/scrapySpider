#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from mopSpider.items import PostItem

check_value = lambda x: x if x else ''


def get_post_item(response):
    sel = Selector(response)
    url = response.url

    post_item = PostItem()
    post_item['url'] = url

    post_id = sel.xpath('//input[@name="use_item_subId"]/@value').extract_first()
    post_item['post_id'] = check_value(post_id)

    path_div = sel.xpath('//p[contains(@class, "mt10")]/a[@title]')
    path_href_list = path_div.xpath('./@href').extract()
    path_text_list = path_div.xpath('./@title').extract()

    post_item['path_text'] = ', '.join(path_text_list)
    post_item['path_href'] = ', '.join([response.urljoin(path_href) for path_href in path_href_list])

    title = sel.xpath('//h1[contains(@class, "subTitle")]').xpath('string(.)').extract_first()
    post_item['title'] = check_value(title)

    publish_date = sel.xpath('//span[@class="c999 mr15"]/text()').extract_first()
    post_item['publish_date'] = check_value(publish_date)

    hits = sel.xpath('//span[contains(@class, "click")]/span[@class="bold"]').xpath('string(.)').extract_first()
    post_item['hits'] = check_value(hits)

    reply_num = sel.xpath('//span[contains(@class, "reply")]/span').xpath('string(.)').extract_first()
    post_item['reply_num'] = check_value(reply_num)

    author_id = sel.xpath('//input[@name="use_item_subId"]/@value').extract_first()
    post_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//a[contains(@class, "userbyName")]').xpath('string(.)').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_href = sel.xpath('//a[contains(@class, "userbyName")]/@href').extract_first()
    post_item['author_href'] = check_value(author_href)

    content = sel.xpath('//div[contains(@class, "article-cont")]').xpath('string(.)').extract_first()
    post_item['content'] = check_value(content)

    picture_hrefs = sel.xpath('//div[contains(@class, "article-cont")]//img/@data-src').extract()
    post_item['picture_hrefs'] = picture_hrefs

    tags = sel.xpath('//dl[@class="tabs-s"]/dd/a/text()').extract()
    post_item['tags'] = tags

    praise_num = sel.xpath('//a[@class="praise"]').xpath('string(.)').extract_first()
    if praise_num and len(praise_num.strip()) > 3:
        post_item['praise_num'] = praise_num.strip()[2:-1]
    else:
        post_item['praise_num'] = '-1'

    recommend_num = sel.xpath('//a[@class="recommendBtn"]').xpath('string(.)').extract_first()
    if recommend_num and len(recommend_num.strip()) > 4:
        post_item['recommend_num'] = recommend_num.strip()[3:-1]
    else:
        post_item['recommend_num'] = '-1'

    collect_num = sel.xpath('//a[@class="favorite"]').xpath('string(.)').extract_first()
    if collect_num and len(collect_num.strip()) > 4:
        post_item['collect_num'] = recommend_num.strip()[3:-1]
    else:
        post_item['collect_num'] = '-1'

    post_item['comment_ids'] = []

    return post_item
