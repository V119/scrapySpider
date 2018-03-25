#!/usr/bin python3
# -*- coding: utf-8 -*-
from scrapy import Selector

from kdnetSpider.items import PostItem
from kdnetSpider.spiders.author import get_author_id_by_href

check_value = lambda x: x if x else ''


def get_page_posts(response, cate_name):
    """
    获取在list中记录的post信息
    :param response:
    :param cate_name:
    :return:
    """
    sel = Selector(response)
    list_span = sel.xpath('//div[@class="list-table"]/table/tbody/tr')
    for post_head in list_span:
        post_status = post_head.xpath('./td[@class="state"]/img/@title').extract_first()
        if not post_status:
            continue
        post_item = PostItem()
        post_item['category'] = check_value(cate_name)
        post_item['post_status'] = check_value(post_status)
        post_title_group = post_head.xpath('./td[@class="subject"]/span[@class="f14px"]/a/@title').extract_first()
        if post_title_group:
            title_s = post_title_group.split('\n')
            title = title_s[0]
            post_time = title_s[2][4:]

            post_item['title'] = check_value(title)
            post_item['post_time'] = check_value(post_time)

        post_url = post_head.xpath('./td[@class="subject"]/span[@class="f14px"]/a/@href').extract_first()
        post_item['post_url'] = response.urljoin(post_url)

        post_name = post_head.xpath('./@name').extract_first()
        post_id = post_name.split('_')[1]
        post_item['post_id'] = check_value(post_id)

        author = post_head.xpath('./td[@class="author"]/a/text()').extract_first()
        author_href = post_head.xpath('./td[@class="author"]/a/@href').extract_first()
        post_item['author'] = check_value(author)
        post_item['author_href'] = check_value(author_href)

        author_id = get_author_id_by_href(author_href)
        post_item['author_id'] = check_value(author_id)

        # 最后更新时间
        last_update = post_head.xpath('./td[@class="lastupdate"]/text()').extract_first()
        post_item['_last_update'] = check_value(last_update).split('|')[0].strip()

        # 回复、点击数
        hits_and_comment = post_head.xpath('./td[contains(@class, "statistics")]/text()').extract_first()
        if hits_and_comment:
            hits = hits_and_comment.split('/')[1].strip()
            comment_num = hits_and_comment.split('/')[0].strip()
        else:
            hits = '-1'
            comment_num = '-1'
        post_item['hits'] = check_value(hits)
        post_item['comment_num'] = check_value(comment_num)

        yield post_item


def get_next_page_url(response):
    """
    获取某个类别下列表的下一页的URL
    :param response:
    :return:
    """
    sel = Selector(response)

    page_div = sel.xpath('//div[@class="pagesmodule"]')
    if page_div:
        page_href = page_div.xpath('./form/a/@href').extract()[-1]
        page_text = page_div.xpath('./form/a/text()').extract()[-1]
        if '下一页' in page_text and page_href:
            return response.urljoin(page_href)

        return None

    return None


# 产生a的占位符
gen_a_text = lambda t, h: '[[(' + str(t) + ')--' + str(h) + ']]'

# 产生表情的占位符
gen_emjo_text = lambda href: '[[(emjo_' + str(href) + ')--'']]'

# 产生表情的占位符
gen_pic_text = lambda href: '[[(pic_' + str(href) + ')--'']]'


def get_post_info(response, post_item):
    sel = Selector(response)

    content_div = sel.xpath('//div[contains(@class, "posts-cont ") or @class="posts-cont"]')
    at_user = content_div.xpath('./span[contains(@class, "name")]/a/text()').extract()
    at_href = content_div.xpath('./span[contains(@class, "name")]/a/@href').extract()

    post_item['at_user'] = at_user
    post_item['at_href'] = at_href

    pictures_href = sel.xpath('//img[@onload]/@src').extract()
    post_item['pictures_href'] = [response.urljoin(picture_href) for picture_href in pictures_href]

    # 产生post文字，链接、图片用占位符表示
    post_text = content_div.xpath('./child::node()').extract()
    text_list = []
    for child_text in post_text:
        content_sel = Selector(text=child_text)
        a_sel = content_sel.xpath('//a[not(@class="tips")]')
        emjo_sel = content_sel.xpath('//img[not(@onload)]')
        pic_sel = content_sel.xpath('//img[@onload]')

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
        else:
            if child_text == '<br>':
                text_list.append('\n')
            else:
                div_text = content_sel.xpath('string(.)').extract_first()
                text_list.append(check_value(div_text))

    post_item['content'] = ''.join(text_list)












