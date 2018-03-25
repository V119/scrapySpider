#!/usr/bin python3
# -*- coding:utf-8 -*-
from scrapy import Selector

from blog163Spider.items import PostItem
from blog163Spider.utils import MD5Utils


check_value = lambda x: x if x else ''


def get_post_item(response):
    sel = Selector(response)
    post_item = PostItem()

    url = response.url
    post_id = get_post_id_by_href(url)
    post_item['id'] = check_value(post_id)
    post_item['post_url'] = check_value(url)

    title = sel.xpath('//div[@class="multicntwrap"]/div[@class="multicnt"]'
                      '//*[contains(@class, "title")]').xpath('string(.)').extract_first()
    post_item['title'] = check_value(title)

    date_time = sel.xpath('//div[@class="multicntwrap"]/div[@class="multicnt"]'
                          '/div/p/span[@class="pleft"]/span[1]').xpath('string(.)').extract_first()
    post_item['date_time'] = check_value(date_time)

    category = sel.xpath('//div[@class="multicntwrap"]/div[@class="multicnt"]/'
                         'div/p/span[@class="pleft"]/a/text()').extract_first()
    post_item['category'] = check_value(category)

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    post_item['key_words'] = check_value(key_words)

    author_href = sel.xpath('//div[@class="m-aboutme"]/div[contains(@class, "nick")]/a/@href').extract_first()
    post_item['author_href'] = check_value(author_href)

    author_name = sel.xpath('//div[@class="m-aboutme"]/div[contains(@class, "nick")]/a/text()').extract_first()
    post_item['author_name'] = check_value(author_name)

    author_id = MD5Utils.md5_code(author_href)
    post_item['author_id'] = author_id

    content_list = sel.xpath('//div[contains(@class, "nbw-blog ")]/p').xpath('string(.)').extract()
    content = ''.join(content_list)
    post_item['content'] = check_value(content)

    picture_hrefs = sel.xpath('//div[contains(@class, "nbw-blog ")]//img/@src').extract()
    post_item['picture_hrefs'] = [response.urljoin(pic_href) for pic_href in picture_hrefs]

    post_href = sel.xpath('//div[contains(@class, "nbw-blog ")]//a/@href').extract()
    post_item['hrefs_in_post'] = [response.urljoin(p_href) for p_href in post_href]

    read_num = sel.xpath('//*[@id="$_spaniReadCount"]').xpath('string(.)').extract_first()
    post_item['read_num'] = check_value(read_num)

    comment_num = sel.xpath('//*[@id="$_spaniCommentCount"]').xpath('string(.)').extract_first()
    post_item['comment_num'] = check_value(comment_num)

    return post_item


def get_post_id_by_href(href):
    if '?' in href:
        href = href.split('?')[0]

    href_s = href.split('/')

    if href_s and len(href) > 5:
        return href_s[5]

    return None
