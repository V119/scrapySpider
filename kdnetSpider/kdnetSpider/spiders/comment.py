#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from scrapy import Selector

from kdnetSpider.items import CommentItem
from kdnetSpider.spiders.author import get_author_id_by_href

check_value = lambda x: x if x else ''

# 产生a的占位符
gen_a_text = lambda t, h: '[[(' + str(t) + ')--' + str(h) + ']]'

# 产生表情的占位符
gen_emjo_text = lambda href: '[[(emjo_' + str(href) + ')--'']]'

# 产生表情的占位符
gen_pic_text = lambda href: '[[(pic_' + str(href) + ')--'']]'


def get_comment_info(response, post_id):
    sel = Selector(response)
    comment_div_list = sel.xpath('//div[contains(@class,"reply-box")]')
    for comment_div in comment_div_list:
        comment_item = CommentItem()
        comment_item['post_id'] = check_value(post_id)

        comment_id = comment_div.xpath('./@id').extract_first()
        comment_item['comment_id'] = check_value(comment_id)

        author_nick = comment_div.xpath('./div[contains(@class, "posted-box")]'
                                        '//div[@class="name"]/span/a/text()').extract_first()
        author_href = comment_div.xpath('./div[contains(@class, "posted-box")]'
                                        '//div[@class="name"]/span/a/@href').extract_first()
        comment_item['author_nick'] = check_value(author_nick)
        comment_item['author_href'] = check_value(author_href)

        author_id = get_author_id_by_href(author_href)
        comment_item['author_id'] = check_value(author_id)

        floor_num = comment_div.xpath('./div[contains(@class, "posted-box")]'
                                      '/div[@class="posted-floor"]//span/a/@id').extract_first()
        if floor_num:
            comment_item['floor_num'] = floor_num[5:]
        else:
            comment_item['floor_num'] = '-1'

        comment_time = comment_div.xpath('./div[contains(@class, "posted-box")]'
                                         '/div[contains(@class, "posted-info")]/text()').extract()[6]
        comment_item['date_time'] = check_value(comment_time).strip()

        content_div = comment_div.xpath('./div[contains(@class, "replycont-box")]//div[@class="replycont-text"]')
        at_user = content_div.xpath('./span[contains(@class, "name")]/a/text()').extract()
        at_href = content_div.xpath('./span[contains(@class, "name")]/a/@href').extract()

        comment_item['at_user'] = at_user
        comment_item['at_href'] = at_href

        pictures_href = content_div.xpath('./img[@onload]/@src | ./*//img[@onload]/@src').extract()
        comment_item['pictures_href'] = [response.urljoin(picture_href) for picture_href in pictures_href]

        # 产生post文字，链接、图片用占位符表示
        post_text = content_div.xpath('./child::node()').extract()
        text_list = []
        quote_comment_id = '-1'
        for child_text in post_text:
            content_sel = Selector(text=child_text)
            a_sel = content_sel.xpath('/html/body/a[not(@class="tips")]')
            emjo_sel = content_sel.xpath('/html/body/img[not(@onload)]')
            pic_sel = content_sel.xpath('/html/body/img[@onload]')
            quote_sel = content_sel.xpath('/html/body/span[@class="quote-cont-box"]')

            if a_sel:
                a_href = a_sel.xpath('./@href').extract_first()
                a_text = a_sel.xpath('text()').extract_first()
                text_list.append(gen_a_text(a_text, a_href))
            elif emjo_sel:
                emjo_src = emjo_sel.xpath('./@src').extract_first()
                text_list.append(check_value(gen_emjo_text(emjo_src) + emjo_sel.xpath('string(.)').extract_first()))
            elif pic_sel:
                pic_src = pic_sel.xpath('./@src').extract_first()
                text_list.append(check_value(gen_pic_text(pic_src) + pic_sel.xpath('string(.)').extract_first()))
            elif quote_sel:
                quote_id = quote_sel.xpath('./span[@class="quote-cont2"]/span[@class="quote-title"]/span/a')\
                    .extract_first()
                if quote_id:
                    quote_comment_id = quote_id.split('#')[-1]
            else:
                if child_text == '<br>':
                    text_list.append('\n')
                else:
                    div_text = content_sel.xpath('string(.)').extract_first()
                    text_list.append(check_value(div_text))

        comment_item['content'] = ''.join(text_list)
        comment_item['quote_comment_id'] = quote_comment_id
        comment_item['parse_time'] = time.time()

        yield comment_item

