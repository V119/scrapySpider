# -*- coding: utf-8 -*-
import json
import uuid

import scrapy
from scrapy import Request
from scrapy import Selector

from doubanTopic.items import PostItem, CommentItem
from doubanTopic.spiders.login_api import get_login_cookie

check_value = lambda x: x if x else ""


class DoubanTopicSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    topic_str = '上海女逃离江西'

    start_urls = ['https://www.douban.com/group/search?cat=1013&q=' + topic_str + '&sort=relevance']
    # start_urls = ['https://www.douban.com/group/topic/83572305/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)

        self.cookies = get_login_cookie(self.start_urls[0])

    def start_requests(self):
        yield Request(self.start_urls[0],
                      cookies=self.cookies,)

    def parse(self, response):
        for item in self.get_article_item(response):
            if item['article_url']:
                yield Request(url=item['article_url'],
                              callback=self.parse_article,
                              meta={
                                  'item': item
                              },
                              cookies=self.cookies,
                              priority=10)
        next_page = self.next_page(response)
        if next_page:
            yield Request(next_page,
                          cookies=self.cookies)

    # def parse(self, response):
    #     item = PostItem()
    #     response.meta['item'] = item
    #     for i_o_r in self.parse_article(response):
    #         yield i_o_r

    # 获取下一页链接
    def next_page(self, response):
        sel = Selector(response)

        next_href = sel.xpath('//div[@class="article"]/div[@class="paginator"]/span[@class="next"]/a/@href')
        if next_href:
            return next_href.extract_first()
        else:
            return None

    # 获取当页所有文章链接
    def get_article_item(self, response):
        sel = Selector(response)
        topic_tr = sel.xpath('//div[@class="topics"]/table/tbody/tr[@class="pl"]')
        for tr in topic_tr:
            title = tr.xpath('./td[@class="td-subject"]/a/@title').extract_first()
            article_url = tr.xpath('./td[@class="td-subject"]/a/@href').extract_first()
            date = tr.xpath('./td[@class="td-time"]/@title').extract_first()
            reply_num = tr.xpath('./td[@class="td-reply"]/span/text()').extract_first()
            group_name = tr.xpath('./td[4]/a/text()').extract_first()

            item = PostItem()
            item['id'] = uuid.uuid4()
            item['keywords'] = self.topic_str
            item['title'] = check_value(title)
            item['article_url'] = check_value(article_url)
            item['date_time'] = check_value(date)
            item['topic'] = check_value(group_name)
            item['reply_num'] = reply_num[:-2] if reply_num and len(reply_num) > 2 else ""

            yield item

    def parse_article(self, response):
        item = response.meta['item']
        sel = Selector(response)
        author = sel.xpath('//div[@class="topic-doc"]/h3/span[@class="from"]/a/text()').extract_first()
        article_list = sel.xpath('//div[@class="topic-content"]/p/text()').extract()
        like_num = sel.xpath('//span[@class="fav-num"]/text()').extract_first()
        recommend_num = sel.xpath('//span[@class="rec-num"]/text()').extract_first()

        item['author_name'] = check_value(author)
        item['article'] = ''.join(article_list) if article_list else ''
        item['like_num'] = like_num if like_num else '0'
        item['recommend_num'] = recommend_num if recommend_num else '0'

        yield item
        # for comment_item_request in self.parse_comment(response, '12345678'):
        for comment_item_request in self.parse_comment(response, item['id']):
            yield comment_item_request

    # 爬取文章的评论
    def parse_comment(self, response, post_id=None):
        if not post_id:
            post_id = response.meta['post_id']

        prise_num_dict = self.get_prise_num_dict(response)
        sel = Selector(response)
        comment_list = sel.xpath('//ul[@id="comments"]/li')
        for comment_sel in comment_list:
            item = CommentItem()
            item['id'] = uuid.uuid4()
            item['post_id'] = post_id
            author = comment_sel.xpath('./div[@class="reply-doc content"]/div/h4/a/text()').extract_first()
            date_time = comment_sel.xpath('./div[@class="reply-doc content"]/div/'
                                          'h4/span[@class="pubtime"]/text()').extract_first()
            comment = comment_sel.xpath('./div[@class="reply-doc content"]/p/text()').extract_first()
            comment_id = comment_sel.xpath('./@id').extract_first()
            prise_num = prise_num_dict.get('c' + comment_id, '0')
            item['author_name'] = check_value(author)
            item['date_time'] = check_value(date_time)
            item['comment'] = check_value(comment)
            item['prise_num'] = str(prise_num)

            yield item

        next_page = self.next_page_comment(response)
        if next_page:
            yield Request(url=next_page,
                          callback=self.parse_comment,
                          meta={
                              "post_id": post_id
                          },
                          cookies=self.cookies,
                          priority=5)

    def next_page_comment(self, response):
        sel = Selector(response)
        next_page_url = sel.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract_first()
        if next_page_url:
            return next_page_url
        else:
            return None

    def get_prise_num_dict(self, response):
        sel = Selector(response)
        comment_vote = sel.re("var\s+commentsVotes\s*=\s*\'(.*)\',")[0]

        if comment_vote:
            vote_obj = json.loads(comment_vote)

            return vote_obj

        return {}

