#!/usr/bin python3
# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import FormRequest
from scrapy import Request
from scrapy import Selector

from nstad.items import *


class NstadSpider(scrapy.Spider):
    name = 'nstad'

    allowed_domains = ['nstad.cn']

    def start_requests(self):
        # 成果项
        for x in range(684):
            params = {
                'pageIndex': str(x),
                'pageSize': '20',
                'cgly': '',
                'hy': '',
                'cgDQ': '',
                'year': ''
            }

            yield FormRequest(
                url='http://www.nstad.cn/ashx/SearchList.ashx',
                formdata=params,
                callback=self.parse_result
            )

        # 工作动态, 暂时只有一页，所以只爬一页,页数通过pageIndex循环
        work_params = {
            'action': 'NewsList',
            'pageIndex': '1',
            'type': 'Work',
            'time': '',
            'title': ''
        }

        yield FormRequest(
            url='http://www.nstad.cn/ashx/Policy.ashx',
            formdata=work_params,
            callback=self.parse_news_list
        )

        # 新闻动态, 5页
        for x in range(1, 6):
            news_params = {
                'action': 'NewsList',
                'pageIndex': str(x),
                'type': 'News',
                'time': '',
                'title': ''
            }

            yield FormRequest(
                url='http://www.nstad.cn/ashx/Policy.ashx',
                formdata=news_params,
                callback=self.parse_news_list
            )

        # 政策
        for x in range(1, 23):
            policy_params = {
                'action': 'InitTable',
                'pageIndex': str(x),
                'kw': 'null',
                'dq': 'null',
                'hy': 'null'
            }

            yield FormRequest(
                url='http://www.nstad.cn/ashx/Policy.ashx',
                formdata=policy_params,
                callback=self.parse_policy_list
            )


    def parse_policy_list(self, response):
        data = response.body.decode()
        sel = Selector(text=data)
        info_divs = sel.xpath('//tr')
        for info_div in info_divs:
            td_divs = info_div.xpath('./td')
            title = td_divs[1].xpath('./a').xpath('string(.)').extract_first()
            href = td_divs[1].xpath('./a/@href').extract_first()
            category = td_divs[2].xpath('string(.)').extract_first()
            date = td_divs[3].xpath('string(.)').extract_first()

            yield Request(
                url=response.urljoin('/' + href),
                callback=self.parse_policy,
                meta={
                    'title': title,
                    'category': category,
                    'date': date
                }
            )


    def parse_policy(self, response):
        title = response.meta['title']
        category = response.meta['category']
        date = response.meta['date']

        policy_item = PolicyItem()
        policy_item['title'] = title
        policy_item['category'] = category
        policy_item['date'] = date

        sel = Selector(response)

        source_div = sel.xpath('//div[@class="time"]').extract_first()
        try:
            p_str = '来源：(.*)'
            p = re.compile(p_str)
            source = p.search(source_div.strip()).group(0).split('：')[-1].strip()
            policy_item['source'] = source
        except:
            raise ValueError(response.url)

        content = sel.xpath('//div[@class="txt"]').xpath('string(.)').extract_first()
        policy_item['content'] = content

        yield policy_item



    def parse_news_list(self, response):
        data = response.body.decode()
        sel = Selector(text=data)

        info_divs = sel.xpath('//ul[@class="list_ul1"]/li')
        for info_div in info_divs:
            href = info_div.xpath('./div[@class="aa2"]/a/@href').extract_first()
            text = info_div.xpath('./div[@class="aa2"]/a').xpath('string(.)').extract_first()
            date = info_div.xpath('./span[@class="time"]/text()').extract_first()

            yield Request(
                url=response.urljoin('/' + href),
                callback=self.parse_news,
                meta={
                    'text': text,
                    'date': date
                }
            )


    def parse_news(self, response):
        title = response.meta['text']
        date = response.meta['date']

        sel = Selector(response)

        news_item = NewsItem()

        news_item['date'] = date
        news_item['title'] = title

        source_div = sel.xpath('//div[@class="time"]').extract_first()
        try:
            p_str = '来源：(.*)'
            p = re.compile(p_str)
            source = p.search(source_div.strip()).group(0).split('：')[-1].strip()
            news_item['source'] = source
        except:
            raise ValueError(response.url)

        content = sel.xpath('//div[@class="txt"]').xpath('string(.)').extract_first()
        news_item['content'] = content

        yield news_item


    def parse_result(self, response):
        data = response.body.decode().split('&&')[0]
        p_str = '{.*?}'
        p = re.compile(p_str)
        values = p.findall(data)

        for value in values:
            p_id_str = 'pid\s*:\s*\'(.*?)\''
            p_date_str = 'lxtime\s*:\s*\'(.*?)\''

            p_id = re.compile(p_id_str)
            p_date = re.compile(p_date_str)

            _id = p_id.search(value).group(0).split(':')[-1][1:-1]
            date = p_date.search(value).group(0).split(':')[-1][1:-1]

            if _id:
                yield Request(
                    url='http://www.nstad.cn/detail.aspx?pid=' + _id,
                    callback=self.parse_result_date,
                    meta={
                        'pid': _id,
                        'date': date
                    }
                )


    def parse_result_date(self, response):
        date = response.meta['date']
        pid = response.meta['pid']
        sel = Selector(response)
        result_item = ResultItem()
        result_item['date'] = date
        result_item['pid'] = pid

        tds = sel.xpath('//table/tr/td')
        for x in range(0, len(tds), 2):
            text = tds[x].xpath('string(.)').extract_first()
            next_text = tds[x + 1].xpath('string(.)').extract_first().strip()

            if '成果名称' in text:
                result_item['title'] = next_text
            elif '关键词' in text:
                result_item['key_words'] = next_text
            elif '成果简介' in text:
                result_item['desc'] = next_text
            else:
                raise ValueError(response.url)

        yield result_item
