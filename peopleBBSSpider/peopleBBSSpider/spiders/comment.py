#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from peopleBBSSpider.items import CommentItem
from peopleBBSSpider.utils import MD5Utils

check_value = lambda x: x if x else ''


def get_comment_list(response):
    sel = Selector(response)
    post_id = sel.xpath('//meta[@name="contentid"]/@content').extract_first()
    comment_div = sel.xpath('//div[@class="replayWrap"]/ul[contains(@class, "replayList")]/li')
    for comment_sel in comment_div:
        comment_item = CommentItem()
        comment_item['post_id'] = post_id

        comment_id = comment_sel.xpath('./ul[@class="author"]/li[@class="replayMsg"]'
                                       '/p[@class="mB"]/@content_id').extract_first()
        comment_item['comment_id'] = check_value(comment_id)

        author_name = comment_sel.xpath('./ul[@class="author"]/li[@class="replayli nickName"]')\
            .xpath('string(.)').extract_first()
        author_href = comment_sel.xpath('./ul[@class="author"]/li[@class="replayli nickName"]/a/@href').extract_first()
        if not author_href:
            author_href = '_'
        author_id = MD5Utils.md5_code(author_href)

        comment_item['author_name'] = check_value(author_name)
        comment_item['author_href'] = check_value(author_href)
        comment_item['author_id'] = check_value(author_id)

        date_time = comment_sel.xpath('./ul[@class="author"]/li[@class="replayMsg"]'
                                      '/p[@class="publishTime"]/text()').extract()[-1]
        comment_item['date_time'] = check_value(date_time).strip()

        floor = comment_sel.xpath('./ul[@class="author"]/li[@class="replayMsg"]/p[@class="publishTime"]'
                                  '/span[@class="floorNum"]/text()').extract_first()
        comment_item['floor'] = check_value(floor).strip()

        prise_num = comment_sel.xpath('./ul[@class="author"]/li[@class="replayMsg"]/p[@class="publishTime"]'
                                      '/span/a/span/text()').extract_first()
        if prise_num and len(prise_num) > 3:
            comment_item['prise_num'] = prise_num[1:-1]
        else:
            comment_item['prise_num'] = '-1'

        comment_item['parent_comment_id'] = '0'

        sub_comment_div = comment_sel.xpath('./ul[@class="subReplay"]/li')
        for i, sub_sel in enumerate(sub_comment_div):
            sub_comment_item = CommentItem()
            sub_comment_item['post_id'] = post_id

            sub_id = comment_id + '_' + str(i)
            sub_comment_item['comment_id'] = sub_id

            sub_author_name = sub_sel.xpath('./div[contains(@class, "subRepCon")]/p[@class="repCon"]')\
                .xpath('string(.)').extract_first()
            sub_comment_item['author_name'] = check_value(sub_author_name)

            sub_author_href = sub_sel.xpath('./div[contains(@class, "subRepCon")]/p[@class="repCon"]'
                                            '/a/@href').extract_first()
            sub_comment_item['author_href'] = check_value(sub_author_href)

            sub_time = sub_sel.xpath('./div[contains(@class, "subRepCon")]/p[@class="repTime"]')\
                .xpath('string(.)').extract_first()
            sub_comment_item['date_time'] = check_value(sub_time)

            sub_comment_item['floor'] = '_'
            sub_comment_item['prise_num'] = '0'

            sub_comment_item['parent_comment_id'] = comment_id

            yield sub_comment_item

        yield comment_item


