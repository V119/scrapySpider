#!/usr/bin python3
# -*- coding:utf-8 -*-
import json

from scrapy import Selector

from doubanGroup.items import CommentItem
from doubanGroup.spiders.post import get_author_id_by_head_src

check_value = lambda x: x if x else ''


def get_comment_list(response, post_id):
    url = response.url
    sel = Selector(response)

    prise_num_dict = get_prise_num_dict(response)

    comment_list = sel.xpath('//ul[@id="comments"]/li')
    for comment_sel in comment_list:
        comment_item = CommentItem()
        comment_item['url'] = url

        comment_id = comment_sel.xpath('./@id').extract_first()
        comment_item['comment_id'] = check_value(comment_id)

        comment_item['post_id'] = post_id

        author_name = comment_sel.xpath('./div[@class="reply-doc content"]'
                                        '/div[@class="bg-img-green"]/h4/a/text()').extract_first()
        comment_item['author_name'] = check_value(author_name)

        author_href = comment_sel.xpath('./div[@class="reply-doc content"]'
                                        '/div[@class="bg-img-green"]/h4/a/@href').extract_first()
        comment_item['author_href'] = check_value(author_href)

        author_pic_src = comment_sel.xpath('./div[@class="user-face"]/a/img/@src').extract_first()
        comment_item['author_id'] = get_author_id_by_head_src(author_pic_src)

        content = comment_sel.xpath('./div[@class="reply-doc content"]/p').xpath('string(.)').extract_first()
        comment_item['content'] = check_value(content)

        pub_time = comment_sel.xpath('./div[@class="reply-doc content"]/div[@class="bg-img-green"]'
                                     '/h4/span[@class="pubtime"]/text()').extract_first()
        comment_item['pub_time'] = check_value(pub_time)

        prise_num = prise_num_dict.get('c' + comment_id, '0')
        comment_item['prise_num'] = str(prise_num)

        quote_content = comment_sel.xpath('./div[@class="reply-doc content"]'
                                          '/div[@class="reply-quote"]/span[@class="all"]/text()').extract_first()
        comment_item['quote_content'] = check_value(quote_content)

        quote_author_name = comment_sel.xpath('./div[@class="reply-doc content"]/div[@class="reply-quote"]'
                                              '/span[@class="pubdate"]/a/text()').extract_first()
        comment_item['quote_author_name'] = check_value(quote_author_name)

        quote_author_href = comment_sel.xpath('./div[@class="reply-doc content"]/div[@class="reply-quote"]'
                                              '/span[@class="pubdate"]/a/@href').extract_first()
        comment_item['quote_author_href'] = check_value(quote_author_href)

        yield comment_item


def get_next_page_href(response):
    sel = Selector(response)
    next_page = sel.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract_first()

    return next_page


def get_prise_num_dict(response):
    sel = Selector(response)
    comment_vote = sel.re("var\s+commentsVotes\s*=\s*\'(.*)\',")[0]

    if comment_vote:
        vote_obj = json.loads(comment_vote)

        return vote_obj

    return {}
