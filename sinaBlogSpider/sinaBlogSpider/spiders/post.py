#!/usr/bin python3
# -*- coding: utf-8 -*-
import re

from scrapy import Selector

from sinaBlogSpider.items import PostItem
from sinaBlogSpider.spiders.author import get_author_id_by_url

check_value = lambda x: x if x else ''


def get_post_item(response):
    sel = Selector(response)

    post_item = PostItem()

    url = response.url
    post_id = get_post_id_by_url(url)

    post_item['url'] = check_value(url)
    post_item['post_id'] = check_value(post_id)

    author_href = sel.xpath('//div[@class="blognavInfo"]/span[@class="last"]/a/@href').extract_first()
    post_item['author_href'] = check_value(author_href)

    author_id = None
    if author_href:
        author_id = get_author_id_by_url(author_href)
    post_item['author_id'] = check_value(author_id)

    author_name = sel.xpath('//*[@id="ownernick"]').xpath('string(.)').extract_first()
    post_item['author_name'] = check_value(author_name)

    title = sel.xpath('//*[@id="articlebody"]/div[@class="articalTitle"]//*[contains(@class, "titName")]') \
        .xpath('string(.)').extract_first()
    post_item['title'] = check_value(title)

    date_time = sel.xpath('//*[@id="articlebody"]/div[@class="articalTitle"]//*[contains(@class, "time")]') \
        .xpath('string(.)').extract_first()
    post_item['date_time'] = check_value(date_time)

    key_words = sel.xpath('//meta[@name="keywords"]/@content').extract_first()
    post_item['key_words'] = check_value(key_words)

    tags = sel.xpath('//td[@class="blog_tag"]/h3/a/text()').extract()
    if tags:
        post_item['tags'] = tags
    else:
        post_item['tags'] = []

    picture_urls = sel.xpath('//*[@id="articlebody"]/div[contains(@class, "articalContent")]//img/@real_src').extract()
    post_item['picture_urls'] = [response.urljoin(pic_url) for pic_url in picture_urls]

    url_in_content = sel.xpath('//*[@id="articlebody"]/div[contains(@class, "articalContent")]//a/@href').extract()
    post_item['url_in_content'] = [response.urljoin(url_c) for url_c in url_in_content]

    content_text = sel.xpath('//*[@id="articlebody"]/div[contains(@class, "articalContent")]').xpath('string(.)') \
        .extract_first()
    post_item['content'] = check_value(content_text)

    share = sel.xpath('//*[@id="articlebody"]/div[@id="share"]')

    get_golden_num = share.xpath('./div[@class="up"]/div[@class="upBox upBox_add"]/p[@class="count"]') \
        .xpath('string(.)').extract_first()
    post_item['get_golden_num'] = check_value(get_golden_num)

    return post_item


def get_num_div_info(response, post_item):
    """
    获得喜欢数、阅读数、评论数、收藏数、转载数
    :param post_item:
    :param response:
    :return:
    """
    body = response.text.replace('}', ',}')
    p1 = re.compile('\"f\":(.*?),')
    # noinspection PyBroadException
    try:
        collect_num = p1.search(body).group(1)
        post_item['collect_num'] = str(collect_num)
    except Exception as e:
        print('收藏数出错：' + e)

    p2 = re.compile('\"d\":(.*?),')
    # noinspection PyBroadException
    try:
        enjoy_num = p2.search(body).group(1)
        post_item['enjoy_num'] = str(enjoy_num)
    except Exception as e:
        print('喜欢数出错：' + e)

    p3 = re.compile('\"z\":(.*?),')
    # noinspection PyBroadException
    try:
        forward_num = p3.search(body).group(1)
        post_item['forward_num'] = str(forward_num)
    except Exception as e:
        print('转发数出错：' + e)

    p4 = re.compile('\"c\":(.*?),')
    # noinspection PyBroadException
    try:
        comment_num = p4.search(body).group(1)
        post_item['comment_num'] = str(comment_num)
    except Exception as e:
        print('收藏数出错：' + e)

    p5 = re.compile('\"r\":(.*?),')
    # noinspection PyBroadException
    try:
        read_num = p5.search(body).group(1)
        post_item['read_num'] = str(read_num)
    except Exception as e:
        print('收藏数出错：' + e)


def get_post_id_by_url(post_url):
    url_split = post_url.split('_')
    if url_split and len(url_split) > 1:
        post_id = url_split[-1].strip().split('.html')[0]

        return post_id

    return None
