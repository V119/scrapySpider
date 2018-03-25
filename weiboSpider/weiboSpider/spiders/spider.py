#!/usr/bin python3
# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy import Spider

from weiboSpider.items import FansItem, BlogItem
from weiboSpider.spiders.get_info import get_user_info, get_fans_ids, get_fans_next_page_url, get_blog_list, \
    get_blog_content_info, get_article_info, get_ajax_next_page, get_ajax_blog, get_ajax_first_page_blog, \
    get_comment_first_url, get_root_comment, get_more_child_comment, get_comment_next_url
from weiboSpider.utils.login_api import get_login_cookie
from weiboSpider.utils.page_info import *


class WeiboSpider(Spider):
    name = 'weibo'

    allowed_domains = [
        'weibo.com'
    ]

    start_urls = [
        'http://d.weibo.com/'
    ]  # 从热门微博开始爬

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
                callback=self.get_hot_user,
                priority=12
            )
            # callback=self.test)
    #
    # def test(self, response):
    #     blog_id = '4062717533357927'
    #     comment_url = get_comment_first_url(blog_id)
    #     yield Request(
    #         url=comment_url,
    #         cookies=self.cookies,
    #         callback=self.parse_comment,
    #         meta={
    #             'blog_id': blog_id
    #         }
    #     )

    # 爬取热门用户的微博信息
    def get_hot_user(self, response):

        hot_html = get_dom_html(response, 'Pl_Core_NewMixFeed__3')

        if hot_html:
            hot_user_urls = Selector(text=hot_html).xpath('//a[@class="W_f14 W_fb S_txt1"]/@href').extract()

            for url in hot_user_urls:
                url_ = url
                if '?' in url:
                    url_ += '&is_all=1#_0'
                else:
                    url_ += '?is_all=1#_0'
                # print(url)
                yield Request(
                    url=url_,
                    cookies=self.cookies,
                    callback=self.parse_user_page,
                    priority=11
                )

    def parse_user_page(self, response):
        # 获取用户的个人信息
        page_id = get_page_conf_info(response, 'page_id')
        user_id = get_page_conf_info(response, 'oid')
        if page_id:
            user_info_url = 'http://weibo.com/p/' + str(page_id) + '/info?mod=pedit_more'
            yield Request(
                url=user_info_url,
                cookies=self.cookies,
                callback=self.parse_user_info,
                meta={
                    'error_count': 0
                },
                priority=10
            )
        else:
            raise AttributeError('no page id')

        # 获取粉丝关注列表ID和主页url
        yield Request(
            url='http://weibo.com/p/' + str(page_id) + '/follow?relate=fans',
            cookies=self.cookies,
            callback=self.parse_fans_list,
            meta={
                'user_id': user_id
            },
            priority=7
        )

        # 关注列表
        yield Request(
            url='http://weibo.com/p/' + str(page_id) + '/follow',
            cookies=self.cookies,
            callback=self.parse_follow_list,
            meta={
                'user_id': user_id
            },
            priority=7
        )

        # 爬取用户微博
        for unflod_url, blog_item in get_blog_list(response):
            if unflod_url:
                yield Request(
                    url=unflod_url,
                    cookies=self.cookies,
                    callback=self.parse_unflod,
                    meta={
                        'blog_item': blog_item
                    },
                    priority=9
                )
            elif 'article_url' in blog_item.fields and blog_item['article_url']:
                yield Request(
                    url=blog_item['article_url'],
                    cookies=self.cookies,
                    callback=self.parse_article,
                    meta={
                        'blog_item': blog_item
                    },
                    priority=9
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
                    },
                    priority=7
                )

                # 请求@的用户主页
                if 'at_url_list' in blog_item and blog_item['at_url_list']:
                    for url in blog_item['at_url_list']:
                        url_ = url
                        if '?' in url:
                            url_ += '&is_all=1#_0'
                        else:
                            url_ += '?is_all=1#_0'
                        # print(url)
                        yield Request(
                            url=url_,
                            cookies=self.cookies,
                            callback=self.parse_user_page,
                            priority=4
                        )

        # 用ajax获取下一页的博客
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
            },
            priority=9
        )

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
                    },
                    priority=10
                )

    def parse_fans_list(self, response):
        user_id = response.meta['user_id']
        fans_ids, fans_urls = get_fans_ids(response)
        # 存储粉丝信息
        for fans_id in fans_ids:
            fans_item = FansItem()
            fans_item['follow_id'] = user_id
            fans_item['fans_id'] = fans_id

            yield fans_item

        # 爬取粉丝的用户主页
        for fans_url in fans_urls:
            url = fans_url
            if '?' in fans_url:
                url += '&is_all=1#_0'
            else:
                url += '?is_all=1#_0'
            yield Request(
                url=url,
                cookies=self.cookies,
                callback=self.parse_user_page,
                priority=4
            )

        next_page_url = get_fans_next_page_url(response)
        # 获取下一页的信息
        if next_page_url:
            yield Request(
                url=next_page_url,
                cookies=self.cookies,
                callback=self.parse_fans_list,
                meta={
                    'user_id': user_id
                },
                priority=6
            )

    def parse_follow_list(self, response):
        user_id = response.meta['user_id']
        fans_ids, fans_urls = get_fans_ids(response)
        # 存储粉丝信息
        for fans_id in fans_ids:
            fans_item = FansItem()
            fans_item['follow_id'] = fans_id
            fans_item['fans_id'] = user_id

            yield fans_item

        # 爬取粉丝的用户主页
        for fans_url in fans_urls:
            url = fans_url
            if '?' in fans_url:
                url += '&is_all=1#_0'
            else:
                url += '?is_all=1#_0'
            yield Request(
                url=url,
                cookies=self.cookies,
                callback=self.parse_user_page,
                priority=4
            )

        next_page_url = get_fans_next_page_url(response)
        # 获取下一页的信息
        if next_page_url:
            yield Request(
                url=next_page_url,
                cookies=self.cookies,
                callback=self.parse_fans_list,
                meta={
                    'user_id': user_id
                },
                priority=4
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
                },
                priority=9
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
            },
            priority=7
        )

        # 请求@的用户主页
        if 'at_url_list' in blog_item and blog_item['at_url_list']:
            for url in blog_item['at_url_list']:
                url_ = url
                if '?' in url:
                    url_ += '&is_all=1#_0'
                else:
                    url_ += '?is_all=1#_0'
                # print(url)
                yield Request(
                    url=url_,
                    cookies=self.cookies,
                    callback=self.parse_user_page,
                    priority=4
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
                        },
                        priority=9
                    )
                elif 'article_url' in blog_item.fields and blog_item['article_url']:
                    yield Request(
                        url=blog_item['article_url'],
                        cookies=self.cookies,
                        callback=self.parse_article,
                        meta={
                            'blog_item': blog_item
                        },
                        priority=9
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
                        },
                        priority=7
                    )

                    # 请求@的用户主页
                    if 'at_url_list' in blog_item and blog_item['at_url_list']:
                        for url in blog_item['at_url_list']:
                            url_ = url
                            if '?' in url:
                                url_ += '&is_all=1#_0'
                            else:
                                url_ += '?is_all=1#_0'
                            # print(url)
                            yield Request(
                                url=url_,
                                cookies=self.cookies,
                                callback=self.parse_user_page,
                                priority=4
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
                            },
                            priority=9
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
                    },
                    priority=9
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
                    },
                    priority=9
                )

        except:
            print('Parse ajax blog error!!  :  ' + Selector(response).text)

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
                    },
                    priority=7
                )
            else:
                yield root_comment

                # 请求评论中评论的用户和@的用户主页
                if 'comment_user_page' in root_comment and root_comment['comment_user_page']:
                    url_ = root_comment['comment_user_page']
                    if '?' in url_:
                        url_ += '&is_all=1#_0'
                    else:
                        url_ += '?is_all=1#_0'
                    # print(url)
                    yield Request(
                        url=url_,
                        cookies=self.cookies,
                        callback=self.parse_user_page,
                        priority=4
                    )

                if 'at_url_list' in root_comment and root_comment['at_url_list']:
                    for url in root_comment['at_url_list']:
                        url_ = url
                        if '?' in url:
                            url_ += '&is_all=1#_0'
                        else:
                            url_ += '?is_all=1#_0'
                        # print(url)
                        yield Request(
                            url=url_,
                            cookies=self.cookies,
                            callback=self.parse_user_page,
                            priority=4
                        )

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
                priority=7
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

            # 请求评论中评论的用户和@的用户主页
            if 'comment_user_page' in more_comment and more_comment['comment_user_page']:
                url_ = more_comment['comment_user_page']
                if '?' in url_:
                    url_ += '&is_all=1#_0'
                else:
                    url_ += '?is_all=1#_0'
                # print(url)
                yield Request(
                    url=url_,
                    cookies=self.cookies,
                    callback=self.parse_user_page,
                    priority=4
                )

            if 'at_url_list' in more_comment and more_comment['at_url_list']:
                for url in more_comment['at_url_list']:
                    url_ = url
                    if '?' in url:
                        url_ += '&is_all=1#_0'
                    else:
                        url_ += '?is_all=1#_0'
                    # print(url)
                    yield Request(
                        url=url_,
                        cookies=self.cookies,
                        callback=self.parse_user_page,
                        priority=4
                    )

        root_comment['child_comment_ids'] = union_list(root_comment['child_comment_ids'], more_comment_list)

        if more_comment_url:
            yield Request(
                url=more_comment_url,
                cookies=self.cookies,
                callback=self.parse_more_comment,
                meta={
                    'root_comment': root_comment,
                    'blog_id': blog_id
                },
                priority=7
            )
        else:
            yield root_comment

            # 请求评论中评论的用户和@的用户主页
            if 'comment_user_page' in root_comment and root_comment['comment_user_page']:
                url_ = root_comment['comment_user_page']
                if '?' in url_:
                    url_ += '&is_all=1#_0'
                else:
                    url_ += '?is_all=1#_0'
                # print(url)
                yield Request(
                    url=url_,
                    cookies=self.cookies,
                    callback=self.parse_user_page,
                    priority=4
                )

            if 'at_url_list' in root_comment and root_comment['at_url_list']:
                for url in root_comment['at_url_list']:
                    url_ = url
                    if '?' in url:
                        url_ += '&is_all=1#_0'
                    else:
                        url_ += '?is_all=1#_0'
                    # print(url)
                    yield Request(
                        url=url_,
                        cookies=self.cookies,
                        callback=self.parse_user_page,
                        priority=4
                    )

