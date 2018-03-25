from scrapy import Selector
from scrapy import Spider

from sinaBlogSpider.spiders.comment import get_comment_info


class Test(Spider):
    name = 'test'

    allowed_domains = ['blog.sina.com.cn']

    # start_urls = ['http://www.sanqin.com/']
    start_urls = ['http://blog.sina.com.cn/s/comment_918c2cc40102x4q8_1.html?comment_v=articlenew']

    def parse(self, response):
        # sel = Selector(response)
        get_comment_info(response, '918c2cc40102x4q8')

        # return item