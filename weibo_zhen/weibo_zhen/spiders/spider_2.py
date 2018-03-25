# import json
#
# from scrapy import Request
# from scrapy import Spider
#
# from weibo_zhen.spiders.get_info import get_blog_list, get_comment_first_url, get_blog_content_info, \
#     get_comment_next_url, get_root_comment, get_more_child_comment
# from weibo_zhen.utils.login_api import get_login_cookie
# from weibo_zhen.utils.page_info import union_list
#
#
# class WeiboSpider(Spider):
#     name = 'weibo_2'
#
#     allowed_domains = [
#         'weibo.com'
#     ]
#
#     start_urls = [
#         'http://weibo.com/u/2387391680?refer_flag=1001030101_&is_all=1',
#     ]
#
#     def __init__(self, name=None, **kwargs):
#         super().__init__(name=None, **kwargs)
#         # if os.path.exists(settings.COOKIE_FILE):
#         #     os.remove(settings.COOKIE_FILE)
#
#         self.cookies = get_login_cookie('http://d.weibo.com/')
#         self.date_str = ['201612', '201611', '201610', '201609', '201608', '201607']
#
#     def parse(self, response):
#         for url_date in self.date_str:
#             url_ = 'http://weibo.com/u/2387391680?is_all=1&stat_date=' \
#                    + url_date \
#                    + '&pids=Pl_Official_MyProfileFeed__22&ajaxpagelet=1&ajaxpagelet_v6=1' \
#                      '&__ref=%2Fu%2F2387391680%3Fis_all%3D1%26stat_date%3D201612%23feedtop'
#             if not self.cookies:
#                 self.cookies = get_login_cookie('http://d.weibo.com/')
#             yield Request(
#                 url=url_,
#                 cookies=self.cookies,
#                 callback=self.parse_blog_ajax,
#                 meta={
#                     'is_first': True
#                 }
#             )
#
#     def parse_blog_ajax(self, response):
#         for unflod_url, blog_item in get_blog_list(response):
#             if unflod_url:
#                 yield Request(
#                     url=unflod_url,
#                     cookies=self.cookies,
#                     callback=self.parse_unflod,
#                     meta={
#                         'blog_item': blog_item
#                     }
#                 )
#             # elif 'article_url' in blog_item.fields and blog_item['article_url']:
#             #     yield Request(
#             #         url=blog_item['article_url'],
#             #         cookies=self.cookies,
#             #         callback=self.parse_article,
#             #         meta={
#             #             'blog_item': blog_item
#             #         }
#             #     )
#             else:
#                 yield blog_item
#
#             # 获取微博的评论
#             blog_id = blog_item['mid']
#             comment_url = get_comment_first_url(blog_id)
#             yield Request(
#                 url=comment_url,
#                 cookies=self.cookies,
#                 callback=self.parse_comment,
#                 meta={
#                     'blog_id': blog_id
#                 }
#             )
#
#     def parse_unflod(self, response):
#         """
#         获取展开全文的微博内容
#         :param response:
#         :return:
#         """
#         blog_item = response.meta['blog_item']
#         body_text = response.text
#         # noinspection PyBroadException
#         try:
#             json_data = json.loads(body_text)
#             html_data = json_data['data']['html']
#             _, info_dict = get_blog_content_info(html_data, True)
#             if info_dict['text_list']:
#                 blog_item['blog_info'] = info_dict['text_list']
#
#             if info_dict['at_url_list']:
#                 blog_item['at_url_list'] = info_dict['at_url_list']
#
#             if info_dict['at_text_list']:
#                 blog_item['at_list'] = info_dict['at_text_list']
#
#             if info_dict['topic_list']:
#                 blog_item['topic_list'] = info_dict['topic_list']
#
#             if info_dict['topic_url_list']:
#                 blog_item['topic_url_list'] = info_dict['topic_url_list']
#
#             if info_dict['article_url_list']:
#                 blog_item['article_url'] = info_dict['article_url_list'][0]
#
#             if info_dict['img_url_list']:
#                 blog_item['picture_url'] = info_dict['img_url_list']
#
#         except:
#             print('parse unflod blog error!!!')
#
#     def parse_comment(self, response):
#         blog_id = response.meta['blog_id']
#
#         for more_comment_url, root_comment in get_root_comment(response, blog_id):
#             # 是否有更多回复的链接，如果有，将所有回复id加到root_comment中
#             if more_comment_url:
#                 yield Request(
#                     url=more_comment_url,
#                     cookies=self.cookies,
#                     callback=self.parse_more_comment,
#                     meta={
#                         'root_comment': root_comment,
#                         'blog_id': blog_id
#                     }
#                 )
#             else:
#                 yield root_comment
#
#         # 获取下一页的comment
#         next_comment_url = get_comment_next_url(response)
#         if next_comment_url:
#             yield Request(
#                 url=next_comment_url,
#                 callback=self.parse_comment,
#                 cookies=self.cookies,
#                 meta={
#                     'blog_id': blog_id
#                 },
#             )
#
#     def parse_more_comment(self, response):
#         root_comment = response.meta['root_comment']
#         blog_id = response.meta['blog_id']
#         parent_comment_id = root_comment['comment_id']
#
#         more_comment_url, comment_list = get_more_child_comment(response, blog_id, parent_comment_id)
#
#         more_comment_list = []
#
#         for more_comment in comment_list:
#             more_comment_list.append(more_comment['comment_id'])
#
#             yield more_comment
#
#         root_comment['child_comment_ids'] = union_list(root_comment['child_comment_ids'], more_comment_list)
#
#         if more_comment_url:
#             yield Request(
#                 url=more_comment_url,
#                 cookies=self.cookies,
#                 callback=self.parse_more_comment,
#                 meta={
#                     'root_comment': root_comment,
#                     'blog_id': blog_id
#                 }
#             )
#         else:
#             yield root_comment
