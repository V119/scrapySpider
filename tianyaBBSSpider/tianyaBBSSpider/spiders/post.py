#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from tianyaBBSSpider.items import PostItem

check_value = lambda x: x if x else ''


def get_post_item(response):
    sel = Selector(response)
    url = response.url

    post_item = PostItem()
    post_item['url'] = url

    author_id = sel.xpath('//input[@name="UserID"]/@value').extract_first()
    post_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//input[@name="UserName"]/@value').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_url = sel.xpath('//ul[contains(@class, "actionBox")]/li'
                           '/a[contains(@class, "homePage")]/@href').extract_first()
    post_item['author_url'] = check_value(author_url)

    blog_id = sel.xpath('//input[@name="BlogID"]/@value').extract_first()
    if not blog_id:
        blog_id = '0000000'

    post_id = sel.xpath('//input[@name="PostID"]/@value').extract_first()
    if not post_id:
        post_id = '000000000'

    post_item['post_id'] = blog_id + '_' + post_id

    title = sel.xpath('//div[@class="article"]/h2/a/@title').extract_first()
    post_item['title'] = check_value(title)

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    post_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//div[contains(@class, "article-tag")]/a/text()').extract()
    post_item['tags'] = tags if tags else []

    date_time = sel.xpath('//div[contains(@class, "article-tag")]/span').xpath('string(.)').extract_first()
    post_item['date_time'] = check_value(date_time)

    create_time = sel.xpath('//input[@name="PostCreateDatetime"]/@value').extract_first()
    post_item['create_time'] = check_value(create_time)

    content = sel.xpath('//div[@class="article"]/div[@class="article-summary articletext"]')\
        .xpath('string(.)').extract()
    post_item['content'] = ''.join(content)

    picture_hrefs = sel.xpath('//div[@class="article"]/div[@class="article-summary articletext"]//img/@src').extract()
    post_item['picture_href'] = [response.urljoin(pic_href) for pic_href in picture_hrefs]

    category = sel.xpath('//div[contains(@class, "article-categories")]/span/a/text()').extract()
    post_item['category'] = category

    comment_num = sel.xpath('//a[@href="#allcomments"]/text()').extract_first()
    if comment_num and len(comment_num.strip()) > 3:
        post_item['comment_num'] = comment_num[3:]
    else:
        post_item['comment_num'] = '-1'

    post_item['comment_ids'] = []

    return post_item






