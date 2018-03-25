# #!/usr/bin python3
# # -*- coding:utf-8 -*-
# from scrapy import Request
# from scrapy import Spider
#
# from doubanGroup.utils.login_api import get_login_cookie
#
#
# class DoubanGroupSpider(Spider):
#     name = 'douban_group'
#
#     allowed_domains = [
#         'weibo.com'
#     ]
#
#     start_urls = [
#         'https://www.douban.com/group/',
#     ]
#
#     def __init__(self, name=None, **kwargs):
#         super().__init__(name=None, **kwargs)
#         # if os.path.exists(settings.COOKIE_FILE):
#         #     os.remove(settings.COOKIE_FILE)
#
#         self.cookies = get_login_cookie(self.start_urls[0])
#
#     def parse(self, response):
#         for url in self.start_urls:
#             if not self.cookies:
#                 self.cookies = get_login_cookie(url)
#             yield Request(
#                 url=url,
#                 cookies=self.cookies,
#                 callback=self.parse_navi,
#                 meta={
#                     'is_first': True
#                 }
#             )
#
#     def parse_navi(self, response):
#         """
#         返回导航栏的类别url
#         :param response:
#         :return:
#         """
