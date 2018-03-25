#!/usr/bin python3
# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy import Spider

from blog_topic.spiders.get_info import get_user_info, get_blog_list, \
    get_blog_content_info, get_article_info, get_ajax_next_page, get_ajax_blog, get_ajax_first_page_blog, \
    get_comment_first_url, get_root_comment, get_more_child_comment, get_comment_next_url
from blog_topic.utils.login_api import get_login_cookie
from blog_topic.utils.page_info import *


class WeiboSpider(Spider):
    name = 'weibo'

    allowed_domains = [
        'weibo.com'
    ]

    start_urls = [
        # 'http://d.weibo.com/'
        # 'http://weibo.com/p/1008087893173742553207b8639dc523fde8a1',
        'http://weibo.com/p/10080845f2d81d6dc780449def3bf17ce66ab2',
        # 'http://weibo.com/p/10080811013b25c6a0284473c9ad2339921203',
    ]  # 从指定的主题开始

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        # if os.path.exists(settings.COOKIE_FILE):
        #     os.remove(settings.COOKIE_FILE)

        self.cookies = get_login_cookie('http://d.weibo.com/')

    def parse(self, response):
        for url_ in self.start_urls:
            if not self.cookies:
                self.cookies = get_login_cookie(url_)
            yield Request(
                url=url_,
                cookies=self.cookies,
                callback=self.parse_blog,
            )

    def parse_blog(self, response):
        for unflod_url, blog_item in get_blog_list(response):
            if unflod_url:
                yield Request(
                    url=unflod_url,
                    cookies=self.cookies,
                    callback=self.parse_unflod,
                    meta={
                        'blog_item': blog_item
                    }
                )
            elif 'article_url' in blog_item.fields and blog_item['article_url']:
                yield Request(
                    url=blog_item['article_url'],
                    cookies=self.cookies,
                    callback=self.parse_article,
                    meta={
                        'blog_item': blog_item
                    }
                )
            else:
                yield blog_item

                # 返回微博时，获取微博的评论信息
                blog_id = blog_item['mid']
                comment_url = get_comment_first_url(blog_id)
                yield Request(
                    url=comment_url,
                    cookies=self.cookies,
                    callback=self.parse_comment,
                    meta={
                        'blog_id': blog_id
                    }
                )

                # 获取用户的信息
                user_url = blog_item['user_href']
                yield Request(
                    url=user_url,
                    cookies=self.cookies,
                    callback=self.parse_user_page
                )

        ajax_next_page_url = get_ajax_next_page(response, 1, 0)
        yield Request(
            url=ajax_next_page_url,
            cookies=self.cookies,
            callback=self.parse_ajax_blog,
            meta={
                'first_page': True,
                'response': response,
                'ajax_page_num': 0,
                'page_num': 1
            }
        )

    def parse_unflod(self, response):
        """
         获取展开全文的微博内容
        :param response:
        :return:
        """
        blog_item = response.meta['blog_item']
        body_text = response.text
        # noinspection PyBroadException
        try:
            json_data = json.loads(body_text)
            html_data = json_data['data']['html']
            _, info_dict = get_blog_content_info(html_data, True)
            if info_dict['text_list']:
                blog_item['blog_info'] = info_dict['text_list']

            if info_dict['at_url_list']:
                blog_item['at_url_list'] = info_dict['at_url_list']

            if info_dict['at_text_list']:
                blog_item['at_list'] = info_dict['at_text_list']

            if info_dict['topic_list']:
                blog_item['topic_list'] = info_dict['topic_list']

            if info_dict['topic_url_list']:
                blog_item['topic_url_list'] = info_dict['topic_url_list']

            if info_dict['article_url_list']:
                blog_item['article_url'] = info_dict['article_url_list'][0]

            if info_dict['img_url_list']:
                blog_item['picture_url'] = info_dict['img_url_list']

        except:
            print('parse unflod blog error!!!')

        if 'article_url' in blog_item.fields and blog_item['article_url']:
            yield Request(
                url=blog_item['article_url'],
                cookies=self.cookies,
                callback=self.parse_article,
                meta={
                    'blog_item': blog_item
                }
            )

    def parse_article(self, response):
        blog_item = response.meta['blog_item']
        article_dict = get_article_info(response)
        if article_dict:
            blog_item['article_date_time'] = article_dict['date_time']
            blog_item['article_title'] = article_dict['title']
            blog_item['article_preface'] = article_dict['preface']
            blog_item['article_content'] = article_dict['content']
            blog_item['article_pic_url_desc'] = article_dict['pic_url_desc']
            blog_item['article_media_url'] = article_dict['media_url']
            blog_item['article_read_num'] = article_dict['read_num']

        yield blog_item

        # 返回微博时，获取微博的评论信息
        blog_id = blog_item['mid']
        comment_url = get_comment_first_url(blog_id)
        yield Request(
            url=comment_url,
            cookies=self.cookies,
            callback=self.parse_comment,
            meta={
                'blog_id': blog_id
            }
        )

        # 获取用户的信息
        user_url = blog_item['user_href']
        yield Request(
            url=user_url,
            cookies=self.cookies,
            callback=self.parse_user_page,
        )

    def parse_comment(self, response):
        blog_id = response.meta['blog_id']

        for more_comment_url, root_comment in get_root_comment(response, blog_id):
            # 是否有更多回复的链接，如果有，将所有回复id加到root_comment中
            if more_comment_url:
                yield Request(
                    url=more_comment_url,
                    cookies=self.cookies,
                    callback=self.parse_more_comment,
                    meta={
                        'root_comment': root_comment,
                        'blog_id': blog_id
                    }
                )
            else:
                yield root_comment

        # 获取下一页的comment
        next_comment_url = get_comment_next_url(response)
        if next_comment_url:
            yield Request(
                url=next_comment_url,
                callback=self.parse_comment,
                cookies=self.cookies,
                meta={
                    'blog_id': blog_id
                },
            )

    def parse_more_comment(self, response):
        root_comment = response.meta['root_comment']
        blog_id = response.meta['blog_id']
        parent_comment_id = root_comment['comment_id']

        more_comment_url, comment_list = get_more_child_comment(response, blog_id, parent_comment_id)

        more_comment_list = []

        for more_comment in comment_list:
            more_comment_list.append(more_comment['comment_id'])

            yield more_comment

        root_comment['child_comment_ids'] = union_list(root_comment['child_comment_ids'], more_comment_list)

        if more_comment_url:
            yield Request(
                url=more_comment_url,
                cookies=self.cookies,
                callback=self.parse_more_comment,
                meta={
                    'root_comment': root_comment,
                    'blog_id': blog_id
                }
            )
        else:
            yield root_comment

    def parse_user_info(self, response):
        """
        得到用户的信息
        :param response:
        :return:
        """
        # 如果发生错误，重新请求该页
        error_count = response.meta['error_count']
        try:
            user_item = get_user_info(response)

            yield user_item
        except ValueError:
            if error_count < 5:
                yield Request(
                    url=response.url,
                    cookies=self.cookies,
                    callback=self.parse_user_info,
                    meta={
                        'error_count': error_count + 1
                    }
                )

    def parse_ajax_blog(self, response):
        # noinspection PyBroadException
        is_first_page = response.meta['first_page']  # 是否是点击按钮的第一页
        ajax_page_num = response.meta['ajax_page_num']
        page_num = response.meta['page_num']
        total_page_response = response.meta['response']
        # noinspection PyBroadException
        try:
            # 先处理当前页面的item，再去获取并请求Request
            if not ajax_page_num == -1:
                json_obj = json.loads(response.text)
                html = json_obj['data']
                has_next_page, blog_list = get_ajax_blog(total_page_response, html, is_first_page=is_first_page)
            else:
                has_next_page = False  # 当ajax_page_num 为-1 时肯定不存在下一页的按钮
                blog_list = get_ajax_first_page_blog(response)

            for unflod_url, blog_item in blog_list:
                if unflod_url:
                    yield Request(
                        url=unflod_url,
                        cookies=self.cookies,
                        callback=self.parse_unflod,
                        meta={
                            'blog_item': blog_item
                        }
                    )
                elif 'article_url' in blog_item.fields and blog_item['article_url']:
                    yield Request(
                        url=blog_item['article_url'],
                        cookies=self.cookies,
                        callback=self.parse_article,
                        meta={
                            'blog_item': blog_item
                        }
                    )
                else:
                    yield blog_item

                    # 返回微博时，获取微博的评论信息
                    blog_id = blog_item['mid']
                    comment_url = get_comment_first_url(blog_id)
                    yield Request(
                        url=comment_url,
                        cookies=self.cookies,
                        callback=self.parse_comment,
                        meta={
                            'blog_id': blog_id
                        }
                    )

                    # 获取用户的信息
                    user_url = blog_item['user_href']
                    yield Request(
                        url=user_url,
                        cookies=self.cookies,
                        callback=self.parse_user_page
                    )

            if ajax_page_num == 1:
                if has_next_page:
                    for x, next_url_page in enumerate(has_next_page[::-1]):  # 从小到大按顺序循环
                        yield Request(
                            url=next_url_page,
                            callback=self.parse_ajax_blog,
                            cookies=self.cookies,
                            meta={
                                'first_page': False,
                                'page_num': x + 2,
                                'response': total_page_response,
                                'ajax_page_num': -1
                            }
                        )
            elif ajax_page_num == 0:
                next_ajax_url = get_ajax_next_page(total_page_response, page_num, ajax_page_num + 1)

                yield Request(
                    url=next_ajax_url,
                    callback=self.parse_ajax_blog,
                    cookies=self.cookies,
                    meta={
                        'first_page': is_first_page,  # 此处若page_num == 1,则is_first_page为true
                        'page_num': page_num,
                        'response': total_page_response,
                        'ajax_page_num': ajax_page_num + 1
                    }
                )
            elif ajax_page_num == -1:
                next_ajax_url = get_ajax_next_page(response, page_num, ajax_page_num + 1)
                yield Request(
                    url=next_ajax_url,
                    callback=self.parse_ajax_blog,
                    cookies=self.cookies,
                    meta={
                        'first_page': False,  # 此处若page_num == -1,则is_first_page为False
                        'page_num': page_num,
                        'response': response,
                        'ajax_page_num': ajax_page_num + 1
                    }
                )

        except:
            print('Parse ajax blog error!!  :  ' + Selector(response).text)

    def parse_user_page(self, response):
        # 获取用户的个人信息
        page_id = get_page_conf_info(response, 'page_id')

        if page_id:
            user_info_url = 'http://weibo.com/p/' + str(page_id) + '/info?mod=pedit_more'
            yield Request(
                url=user_info_url,
                cookies=self.cookies,
                callback=self.parse_user_info,
                meta={
                    'error_count': 0
                }
            )
        else:
            raise AttributeError('no page id')

    def parse_user_info(self, response):
        """
        得到用户的信息
        :param response:
        :return:
        """
        # 如果发生错误，重新请求该页
        error_count = response.meta['error_count']
        try:
            user_item = get_user_info(response)

            yield user_item
        except ValueError:
            if error_count < 5:
                yield Request(
                    url=response.url,
                    cookies=self.cookies,
                    callback=self.parse_user_info,
                    meta={
                        'error_count': error_count + 1
                    }
                )
