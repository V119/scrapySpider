import json

from scrapy import Request
from scrapy import Selector
from scrapy import Spider

from weiboSpider.spiders import spider
from weiboSpider.spiders.get_info import get_blog_list, get_blog_content_info, get_root_comment, get_more_child_comment
from weiboSpider.utils.login_api import get_login_cookie


class Test(Spider):
    name = 'test'

    # start_urls = ['http://weibo.com/p/1005056091206703/home?from=page_100505_profile&wvr=6&mod=data&is_all=1#place']
    start_urls = [
        'http://weibo.com/aj/v6/comment/big?ajwvr=6&more_comment=big&root_comment_id=4045346818309445&is_child_comment=ture&last_child_comment_id=4045347498198914&id=4045295190574821&from=singleWeiBo']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        # if os.path.exists(settings.COOKIE_FILE):
        #     os.remove(settings.COOKIE_FILE)

        self.cookies = get_login_cookie('http://d.weibo.com/')

    def parse(self, response):
        for url_ in self.start_urls:
            if not self.cookies:
                self.cookies = get_login_cookie(url_)
            yield Request(url_,
                          cookies=self.cookies,
                          callback=self.get_hot_user)

    def get_hot_user(self, response):
        # count = 0
        mid = '4045295190574821'
        for comment_item in get_more_child_comment(response, mid, '123333'):
            # print('url:  ' + more_url)

            yield comment_item
