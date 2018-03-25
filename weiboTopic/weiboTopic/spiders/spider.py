#!/usr/bin python3
# -*- coding: utf-8 -*-
import json
import uuid

from scrapy import Request
from scrapy import Spider

from weiboTopic.items import PostItem, CommentItem
from weiboTopic.utils.login import get_cookies


class WeiboSpider(Spider):
    name = 'weiboTopic'

    allowed_domains = [
        'weibo.com'
    ]

    query_str = '设立雄安新区'

    start_urls = [
        'https://m.weibo.cn/api/container/getIndex?',
    ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        # if os.path.exists(settings.COOKIE_FILE):
        #     os.remove(settings.COOKIE_FILE)
        cookie_path = 'D:/project/spiderProject/weiboTopic/weiboTopic/utils/cookie.data'
        self.cookies = get_cookies(cookie_path)

    def start_requests(self):
        params = {
            'type': 'all',
            'queryVal': '设立雄安新区',
            'luicode': '10000011',
            'lfid': '106003type%3D1',
            'title': '设立雄安新区',
            'containerid': '100103type%3D1%26q%3D设立雄安新区'

        }
        param_list = []
        for k in params:
            param_list.append(k + '=' + params[k])

        url = self.start_urls[0] + '&'.join(param_list)
        yield Request(url=url,
                      callback=self.parse_content,
                      cookies=self.cookies,
                      meta={
                          'url_prefix': url
                      })

    def parse(self, response):
        json_obj = json.loads(response.text)
        # data-cards[i]-mblog-内容：text

        print(json_obj)

    def parse_content(self, response):
        json_obj = json.loads(response.text)
        url_prefix = response.meta['url_prefix']
        if json_obj['ok'] == 1:
            mblog_list = []

            # 最新微博
            cards = json_obj['data']['cards']
            if len(cards) == 3:
                if 'mblog' in cards[0]:
                    new_blog = cards[0]['mblog']
                    mblog_list.append(new_blog)

                blog_group = cards[2]['card_group']
            else:
                blog_group = cards[0]['card_group']
            for blog in blog_group:
                s_mblog = blog.get('mblog')
                if s_mblog:
                    mblog_list.append(s_mblog)

            if mblog_list:
                for mblog in mblog_list:
                    blog_item = PostItem()
                    blog_item['id'] = uuid.uuid4()
                    blog_item['blog_id'] = mblog.get('mid', mblog.get('id', '0'))
                    blog_item['blog'] = mblog.get('text', '')
                    blog_item['page_url'] = mblog.get('page_info', {}).get('page_url', '')
                    blog_item['page_type'] = mblog.get('page_info', {}).get('type', '')
                    blog_item['date'] = mblog.get('created_at', '')
                    blog_item['forward_num'] = mblog.get('reposts_count', 0)
                    blog_item['comment_num'] = mblog.get('comments_count', 0)
                    blog_item['prise_num'] = mblog.get('attitudes_count', 0)

                    user = mblog.get('user', {})
                    blog_item['user_id'] = user.get('id', '0')
                    blog_item['user_name'] = user.get('screen_name', '')
                    blog_item['description'] = user.get('description', '')
                    blog_item['gender'] = user.get('gender', '')
                    blog_item['follow_num'] = user.get('follow_count', 0)
                    blog_item['verified'] = user.get('followers_count', '')
                    blog_item['fans_num'] = user.get('verified', 0)
                    blog_item['verified_reason'] = user.get('verified_reason', '')
                    blog_item['verified_type'] = user.get('verified_type', '')
                    blog_item['verified_type_ext'] = user.get('verified_type_ext', '')

                    yield blog_item

                    # 获取评论
                    if int(blog_item['comment_num']) > 0 and blog_item['blog_id'] != '0':
                        comment_url = 'https://m.weibo.cn/api/comments/show?id=' + blog_item['blog_id'] + '&page=1'
                        yield Request(
                            url=comment_url,
                            callback=self.parse_comment,
                            meta={
                                'blog_id': blog_item['id'],
                                'm_id': blog_item['blog_id'],
                                'current_index': 1
                            },
                            priority=2,
                            dont_filter=True
                        )
            next_page = json_obj['data']['cardlistInfo']['page']
            if next_page and next_page != 'null':
                yield Request(
                    url=url_prefix + '&page=' + str(next_page),
                    callback=self.parse_content,
                    cookies=self.cookies,
                    meta={
                        'url_prefix': url_prefix
                    },
                    dont_filter=True
                )



    def parse_comment(self, response):
        blog_id = response.meta['blog_id']
        current_index = response.meta['current_index']
        m_id = response.meta['m_id']
        json_obj = json.loads(response.text)
        status = json_obj['ok']
        if status == 1:
            data_list = json_obj['data']['data']
            max_index = json_obj['data']['max']
            for data in data_list:
                comment_item = CommentItem()
                comment_item['id'] = uuid.uuid4()
                comment_item['blog_id'] = blog_id
                comment_item['comment'] = data.get('text', '')
                comment_item['date'] = data.get('created_at', '')
                comment_item['comment_id'] = data.get('id', '')
                comment_item['prise_num'] = data.get('like_counts', 0)
                comment_item['source'] = data.get('source', 0)

                user_data = data.get('user', {})
                comment_item['user_id'] = user_data.get('id', '0')
                comment_item['user_name'] = user_data.get('screen_name', '')
                comment_item['verified'] = user_data.get('verified', '')
                comment_item['verified_type'] = user_data.get('verified_type', '')
                comment_item['verified_type_ext'] = user_data.get('verified_type_ext', '')

                yield comment_item

            if max_index > current_index:
                current_index += 1
                yield Request(
                    url='https://m.weibo.cn/api/comments/show?id=' + m_id + '&page=' + str(current_index),
                    callback=self.parse_comment,
                    meta={
                        'blog_id': blog_id,
                        'm_id': m_id,
                        'current_index': current_index
                    },
                    priority=2,
                    dont_filter=True,
                )
