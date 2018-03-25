#! /usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from mopSpider.items import CommentItem

check_value = lambda x: x if x else ''


def get_comment_item(response, post_id):
    sel = Selector(response)

    reply_list = sel.xpath('//div[@class="reply-list"]/ul/li')

    for reply_sel in reply_list:
        comment_item = CommentItem()
        comment_item['post_id'] = post_id

        comment_id = reply_sel.xpath('./div[contains(@class, "reply_inner")]/@replyid').extract_first()
        comment_item['comment_id'] = check_value(comment_id)

        user_id = reply_sel.xpath('./div[contains(@class, "nameImg")]/div/a/@uid').extract_first()
        if not user_id:
            user_id = '000000000'   # 匿名用户
            user_href = ''
            user_name = '匿名用户'
        else:
            user_href = reply_sel.xpath('./div[contains(@class, "reply_inner")]'
                                        '/div[@class="c999 oh"]/div[@class="fl"]/p/a/@href').extract_first()
            user_name = reply_sel.xpath('./div[contains(@class, "reply_inner")]'
                                        '/div[@class="c999 oh"]/div[@class="fl"]/p/a/text()').extract_first()
        comment_item['user_id'] = user_id

        comment_item['user_href'] = check_value(user_href)
        comment_item['user_name'] = check_value(user_name)

        date_time = reply_sel.xpath('./div[contains(@class, "reply_inner")]/div[@class="c999 oh"]'
                              '/div[contains(@class, "time")]/text()').extract_first()
        comment_item['date_time'] = check_value(date_time).strip()

        content = reply_sel.xpath('./div[contains(@class, "reply_inner")]'
                                  '/div[contains(@class, "inner-txt")]').xpath('string(.)').extract_first()
        comment_item['content'] = check_value(content)

        picture_hrefs = reply_sel.xpath('./div[contains(@class, "reply_inner")]'
                                  '/div[contains(@class, "inner-txt")]//img/@src').extract()
        comment_item['picture_hrefs'] = [response.urljoin(p_href) for p_href in picture_hrefs]

        praise_num = reply_sel.xpath('./div[contains(@class, "reply_inner")]/div[@class="mt10 c999 lh20 oh"]'
                                     '/div[@class="fr"]/strong').xpath('string(.)').extract_first()
        comment_item['praise_num'] = check_value(praise_num).strip()

        reply_num = reply_sel.xpath('./div[contains(@class, "reply_inner")]/div[@class="mt10 c999 lh20 oh"]'
                                     '/div[@class="fr"]/a/@num').extract_first()
        comment_item['reply_num'] = check_value(reply_num)

        floor = reply_sel.xpath('./div[contains(@class, "reply_inner")]/div[@class="c999 oh"]'
                                '/div[@class="fl"]/p/span[@class="floor"]/text()').extract_first()
        comment_item['floor_num'] = check_value(floor)

        yield comment_item
